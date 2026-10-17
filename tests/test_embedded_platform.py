"""Tests verifying Fix 7: Embedded Platform Support Message.

Done when: An unsupported platform (glibc < 2.39, macOS < 15) gets a clear message,
'no embedded build for this platform, use Docker or a server', not a pip build error.
"""
import sys
import platform
from unittest.mock import patch
import pytest

from guard_cli.backend import (
    EmbeddedBackend,
    check_embedded_platform_support,
)


def test_embedded_platform_glibc_below_2_39():
    """Linux with glibc < 2.39 must produce clear unsupported platform message."""
    with patch.object(sys, "platform", "linux"), \
         patch.object(sys, "version_info", (3, 12, 1)), \
         patch.object(platform, "libc_ver", return_value=("glibc", "2.35")):
        ok, msg = check_embedded_platform_support()
        assert ok is False
        assert "no embedded build for this platform, use Docker or a server" in msg
        assert "glibc 2.39" in msg

        with pytest.raises(RuntimeError, match="no embedded build for this platform, use Docker or a server"):
            EmbeddedBackend()


def test_embedded_platform_macos_below_15():
    """macOS < 15 must produce clear unsupported platform message."""
    with patch.object(sys, "platform", "darwin"), \
         patch.object(sys, "version_info", (3, 12, 1)), \
         patch.object(platform, "mac_ver", return_value=("14.6.1", ("", "", ""), "")):
        ok, msg = check_embedded_platform_support()
        assert ok is False
        assert "no embedded build for this platform, use Docker or a server" in msg
        assert "macOS 15" in msg

        with pytest.raises(RuntimeError, match="no embedded build for this platform, use Docker or a server"):
            EmbeddedBackend()


def test_embedded_platform_non_posix():
    """Unsupported OS (e.g. win32) produces clear message."""
    with patch.object(sys, "platform", "win32"), \
         patch.object(sys, "version_info", (3, 12, 1)):
        ok, msg = check_embedded_platform_support()
        assert ok is False
        assert "no embedded build for this platform, use Docker or a server" in msg


def test_embedded_import_error_catches_glibc_link_failure():
    """Failed import/symbol loading yields clear Docker or server guidance."""
    with patch("guard_cli.backend.check_embedded_platform_support", return_value=(True, "")):
        backend = EmbeddedBackend.__new__(EmbeddedBackend)
        backend.db_path = "/tmp/test.rdb"
        backend._client = None

        with patch("builtins.__import__", side_effect=OSError("/lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.39' not found")):
            with pytest.raises(RuntimeError, match="no embedded build for this platform, use Docker or a server"):
                backend.connect()
