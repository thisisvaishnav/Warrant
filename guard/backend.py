"""Backend abstraction layer for Guard (Work Package B).

Provides:
- GraphBackend interface (ABC)
- ServerBackend: connects to existing FalkorDB server (e.g. localhost:6379)
- DockerBackend: manages dedicated docker container 'guard-falkordb' on port 6390
- EmbeddedBackend: manages embedded FalkorDBLite in ~/.guard/data/ (Python 3.12+)
- Backend resolution and fallback chain
- Configuration storage in .guard/config.toml
"""
from __future__ import annotations
import abc
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore


DEFAULT_SERVER_HOST = "localhost"
DEFAULT_SERVER_PORT = 6379
DEFAULT_DOCKER_PORT = 6390
DEFAULT_DOCKER_CONTAINER = "guard-falkordb"
DEFAULT_DOCKER_IMAGE = "falkordb/falkordb:latest"
DEFAULT_DOCKER_VOLUME = "guard-data:/data"


def get_repo_graph_name(repo_path: str | Path | None = None) -> str:
    """Derive a unique, safe FalkorDB graph name from the repository path."""
    if repo_path is None:
        p = Path.cwd()
    else:
        p = Path(repo_path).resolve()
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", p.name.lower()).strip("_")
    if not clean_name:
        clean_name = "repo"
    path_hash = hashlib.sha256(str(p).encode("utf-8")).hexdigest()[:8]
    return f"guard_{clean_name}_{path_hash}"


def _parse_simple_toml(content: str) -> dict[str, Any]:
    """Fallback simple TOML parser for basic [section] key=val configs."""
    result: dict[str, Any] = {}
    current_section = result
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            sec = line[1:-1].strip()
            result[sec] = {}
            current_section = result[sec]
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            # Parse primitives
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False
            elif val.isdigit():
                val = int(val)
            current_section[key] = val
    return result


def load_config(repo_path: str | Path | None = None) -> dict[str, Any]:
    """Loads configuration from .guard/config.toml if present."""
    base = Path(repo_path).resolve() if repo_path else Path.cwd()
    cfg_file = base / ".guard" / "config.toml"
    if not cfg_file.exists():
        return {}
    content = cfg_file.read_text(encoding="utf-8")
    if tomllib is not None:
        try:
            return tomllib.loads(content)
        except Exception:
            return _parse_simple_toml(content)
    return _parse_simple_toml(content)


def save_config(repo_path: str | Path, config: dict[str, Any]) -> Path:
    """Saves configuration to .guard/config.toml."""
    base = Path(repo_path).resolve()
    guard_dir = base / ".guard"
    guard_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = guard_dir / "config.toml"

    lines: list[str] = [
        "# Guard configuration file - automatically generated",
        "",
    ]
    for section, values in config.items():
        if isinstance(values, dict):
            lines.append(f"[{section}]")
            for k, v in values.items():
                if isinstance(v, bool):
                    lines.append(f"{k} = {str(v).lower()}")
                elif isinstance(v, (int, float)):
                    lines.append(f"{k} = {v}")
                else:
                    lines.append(f'{k} = "{v}"')
            lines.append("")
        else:
            if isinstance(values, bool):
                lines.append(f"{section} = {str(values).lower()}")
            elif isinstance(values, (int, float)):
                lines.append(f"{section} = {values}")
            else:
                lines.append(f'{section} = "{values}"')

    cfg_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return cfg_file


class GraphBackend(abc.ABC):
    """Abstract interface for FalkorDB backends."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of backend: 'server', 'docker', or 'embedded'."""
        pass

    @abc.abstractmethod
    def connect(self) -> Any:
        """Return connected FalkorDB client."""
        pass

    @abc.abstractmethod
    def is_healthy(self) -> bool:
        """Check if backend is reachable and responsive to queries."""
        pass

    @abc.abstractmethod
    def describe(self) -> dict[str, Any]:
        """Return diagnostic description dictionary."""
        pass

    @abc.abstractmethod
    def get_graph(self, graph_name: str) -> Any:
        """Return FalkorDB graph object for given name."""
        pass

    def close(self) -> None:
        """Release any held resources."""
        pass


class ServerBackend(GraphBackend):
    """Connects to an existing FalkorDB server instance."""

    def __init__(self, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT):
        self.host = host
        self.port = int(port)
        self._client: Any = None

    @property
    def name(self) -> str:
        return "server"

    def connect(self) -> Any:
        if self._client is None:
            from falkordb import FalkorDB
            self._client = FalkorDB(host=self.host, port=self.port)
        return self._client

    def is_healthy(self) -> bool:
        try:
            client = self.connect()
            g = client.select_graph("guard_healthcheck")
            res = g.query("RETURN 1 AS n")
            return bool(res and res.result_set)
        except Exception:
            self._client = None
            return False

    def describe(self) -> dict[str, Any]:
        healthy = self.is_healthy()
        return {
            "type": "server",
            "host": self.host,
            "port": self.port,
            "healthy": healthy,
            "connection_str": f"{self.host}:{self.port}",
        }

    def get_graph(self, graph_name: str) -> Any:
        return self.connect().select_graph(graph_name)

    def close(self) -> None:
        self._client = None


class DockerBackend(GraphBackend):
    """Manages a dedicated FalkorDB container running via Docker on port 6390."""

    def __init__(
        self,
        port: int = DEFAULT_DOCKER_PORT,
        container_name: str = DEFAULT_DOCKER_CONTAINER,
        image: str = DEFAULT_DOCKER_IMAGE,
        volume: str = DEFAULT_DOCKER_VOLUME,
    ):
        self.port = int(port)
        self.container_name = container_name
        self.image = image
        self.volume = volume
        self._client: Any = None

    @property
    def name(self) -> str:
        return "docker"

    @staticmethod
    def docker_available() -> bool:
        """Check if docker CLI is available and docker daemon is reachable."""
        if not shutil.which("docker"):
            return False
        try:
            res = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return res.returncode == 0
        except Exception:
            return False

    def container_status(self) -> str | None:
        """Returns 'running', 'exited', or None if container does not exist."""
        if not shutil.which("docker"):
            return None
        try:
            res = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name=^/{self.container_name}$", "--format", "{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            out = res.stdout.strip()
            if not out:
                return None
            if out.lower().startswith("up"):
                return "running"
            return "exited"
        except Exception:
            return None

    def start_container(self) -> bool:
        """Starts existing container or launches new container."""
        if not self.docker_available():
            return False

        status = self.container_status()
        if status == "running":
            return True

        if status == "exited":
            # Restart existing container
            res = subprocess.run(
                ["docker", "start", self.container_name],
                capture_output=True,
                text=True,
                timeout=15,
            )
            if res.returncode != 0:
                return False
        else:
            # Run new container
            cmd = [
                "docker", "run", "-d",
                "--name", self.container_name,
                "-v", self.volume,
                "-p", f"{self.port}:6379",
                self.image,
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode != 0:
                return False

        # Wait up to 10 seconds for container to answer healthcheck
        for _ in range(20):
            time.sleep(0.5)
            if self.is_healthy():
                return True
        return self.is_healthy()

    def connect(self) -> Any:
        if self._client is None:
            from falkordb import FalkorDB
            self._client = FalkorDB(host="localhost", port=self.port)
        return self._client

    def is_healthy(self) -> bool:
        try:
            client = self.connect()
            g = client.select_graph("guard_healthcheck")
            res = g.query("RETURN 1 AS n")
            return bool(res and res.result_set)
        except Exception:
            self._client = None
            return False

    def describe(self) -> dict[str, Any]:
        status = self.container_status()
        healthy = self.is_healthy()
        return {
            "type": "docker",
            "container": self.container_name,
            "port": self.port,
            "image": self.image,
            "volume": self.volume,
            "status": status or "not_found",
            "healthy": healthy,
        }

    def get_graph(self, graph_name: str) -> Any:
        return self.connect().select_graph(graph_name)

    def close(self) -> None:
        self._client = None


class EmbeddedBackend(GraphBackend):
    """Manages an embedded FalkorDBLite instance (Python 3.12+)."""

    def __init__(self, data_path: str | Path | None = None):
        if sys.platform not in ("darwin", "linux") and not sys.platform.startswith("linux"):
            raise RuntimeError(
                f"Embedded backend (FalkorDBLite) is not supported on platform '{sys.platform}'. "
                f"FalkorDBLite only supports Linux and macOS. "
                f"Please use Docker backend ('guard init --backend docker') or Server backend ('guard init --backend server')."
            )

        if sys.version_info < (3, 12):
            raise RuntimeError(
                f"Embedded backend (FalkorDBLite) requires Python 3.12 or newer. "
                f"Current interpreter is Python {sys.version.split()[0]}. "
                f"Try: uv tool install --python 3.12 guard-cli, or use Docker/Server backend."
            )

        if data_path is None:
            base_dir = Path.home() / ".guard" / "data"
            base_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = base_dir / "falkordb.rdb"
        else:
            self.db_path = Path(data_path).resolve()
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._client: Any = None

    @property
    def name(self) -> str:
        return "embedded"

    def connect(self) -> Any:
        if self._client is None:
            # Check import paths (redislite vs falkordblite)
            try:
                from redislite import FalkorDB
            except ImportError:
                try:
                    from falkordblite import FalkorDB  # type: ignore
                except ImportError as err:
                    raise ImportError(
                        "falkordblite is not installed. Install with: pip install 'guard-cli[embedded]'"
                    ) from err

            self._client = FalkorDB(dbfilename=str(self.db_path))
        return self._client

    def is_healthy(self) -> bool:
        try:
            client = self.connect()
            g = client.select_graph("guard_healthcheck")
            res = g.query("RETURN 1 AS n")
            return bool(res and res.result_set)
        except Exception:
            self._client = None
            return False

    def describe(self) -> dict[str, Any]:
        healthy = self.is_healthy()
        return {
            "type": "embedded",
            "data_path": str(self.db_path),
            "python_version": sys.version.split()[0],
            "healthy": healthy,
        }

    def get_graph(self, graph_name: str) -> Any:
        return self.connect().select_graph(graph_name)

    def close(self) -> None:
        self._client = None


def resolve_backend(
    preference: str | None = None,
    repo_path: str | Path | None = None,
    autostart: bool = True,
) -> GraphBackend:
    """Resolve backend using preference, repository config, or fallback chain.

    Fallback chain order:
    1. Explicit preference or .guard/config.toml preference
    2. Existing server (localhost:6379 or configured FALKORDB_PORT)
    3. Docker container (guard-falkordb on port 6390)
    4. Embedded (FalkorDBLite, Python 3.12+)
    """
    cfg = load_config(repo_path)
    b_cfg = cfg.get("backend", {})

    pref = preference or b_cfg.get("type")
    host = b_cfg.get("host") or os.getenv("FALKORDB_HOST", DEFAULT_SERVER_HOST)
    port = int(b_cfg.get("port") or os.getenv("FALKORDB_PORT", DEFAULT_SERVER_PORT))

    # 1. Explicit preference
    if pref:
        pref = pref.lower().strip()
        if pref == "server":
            return ServerBackend(host=host, port=port)
        elif pref == "docker":
            d_port = int(b_cfg.get("port", DEFAULT_DOCKER_PORT))
            b = DockerBackend(port=d_port)
            if autostart and not b.is_healthy():
                b.start_container()
            return b
        elif pref == "embedded":
            return EmbeddedBackend()
        else:
            raise ValueError(f"Unknown backend preference: '{pref}'. Choose 'server', 'docker', or 'embedded'.")

    # 2. Existing server check
    srv = ServerBackend(host=host, port=port)
    if srv.is_healthy():
        return srv

    # 3. Docker check
    if DockerBackend.docker_available():
        dock = DockerBackend(port=DEFAULT_DOCKER_PORT)
        if autostart:
            if dock.start_container() and dock.is_healthy():
                return dock
        elif dock.is_healthy():
            return dock

    # 4. Embedded fallback check
    if sys.version_info >= (3, 12):
        try:
            emb = EmbeddedBackend()
            if emb.is_healthy():
                return emb
        except Exception:
            pass

    # Default fallback: return ServerBackend so caller receives connection details/errors
    return srv
