"""Mutant generator for Flask target repo.
Generates 40 semantic mutations across core Flask modules.
Each mutant is saved as a unified diff file in evals/mutants/.
Generates frozen evals/split.json (R3 Goodhart rule: frozen before tuning).
"""
import os
import hashlib
import json
import subprocess
from pathlib import Path

MUTANTS_DIR = Path("evals/mutants")
SPLIT_FILE = Path("evals/split.json")
REPO_ROOT = Path("target_repos/flask")


def find_mutation_candidates():
    """Scans Flask source files to find reliable semantic mutation candidates."""
    root = REPO_ROOT / "src/flask"
    candidates = []

    for py_file in sorted(root.rglob("*.py")):
        if py_file.name.startswith("__"):
            continue
        rel = str(py_file.relative_to(REPO_ROOT))
        text = py_file.read_text(encoding="utf-8")
        lines = text.splitlines()

        for idx, line in enumerate(lines):
            stripped = line.strip()
            # 1. Flip boolean returns
            if stripped in ("return True", "return False"):
                rep = "return False" if stripped == "return True" else "return True"
                candidates.append((rel, idx + 1, line, line.replace(stripped, rep), f"flip bool at {rel}:{idx+1}"))
            # 2. Return None on short return statements
            elif stripped.startswith("return ") and stripped != "return None" and len(stripped) < 45 and not stripped.endswith(":"):
                candidates.append((rel, idx + 1, line, line.replace(stripped, "return None"), f"return None at {rel}:{idx+1}"))
            # 3. Invert 'if not X:' -> 'if X:'
            elif stripped.startswith("if not ") and stripped.endswith(":") and len(stripped) < 50:
                rep = stripped.replace("if not ", "if ", 1)
                candidates.append((rel, idx + 1, line, line.replace(stripped, rep), f"invert if not at {rel}:{idx+1}"))
            # 4. Invert 'is not' -> 'is'
            elif stripped.startswith("if ") and not stripped.startswith("if not ") and stripped.endswith(":") and " is not " in stripped and len(stripped) < 55:
                rep = stripped.replace(" is not ", " is ", 1)
                candidates.append((rel, idx + 1, line, line.replace(stripped, rep), f"invert is not at {rel}:{idx+1}"))
            # 5. Invert '==' -> '!='
            elif stripped.startswith("if ") and " == " in stripped and stripped.endswith(":") and len(stripped) < 50:
                rep = stripped.replace(" == ", " != ", 1)
                candidates.append((rel, idx + 1, line, line.replace(stripped, rep), f"invert == at {rel}:{idx+1}"))

    return candidates


def generate_diff(file_rel_path: str, line_no: int, old_line: str, new_line: str) -> str:
    full_path = REPO_ROOT / file_rel_path
    lines = full_path.read_text(encoding="utf-8").splitlines()
    assert lines[line_no - 1] == old_line, f"Mismatch at {file_rel_path}:{line_no}"

    lines[line_no - 1] = new_line
    mutated_content = "\n".join(lines) + "\n"

    # Write mutated file temporarily to generate git diff
    full_path.write_text(mutated_content, encoding="utf-8")
    proc = subprocess.run(
        ["git", "diff", "--", file_rel_path],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    # Restore original content
    proc_reset = subprocess.run(
        ["git", "checkout", "--", file_rel_path],
        cwd=str(REPO_ROOT),
        capture_output=True,
    )
    diff_text = proc.stdout
    assert diff_text.strip(), f"Generated empty diff for {file_rel_path}:{line_no}"
    return diff_text


def select_diverse_mutants(candidates, target_count=40):
    """Picks target_count mutants distributed evenly across files."""
    by_file = {}
    for c in candidates:
        by_file.setdefault(c[0], []).append(c)

    selected = []
    # Round-robin selection across files
    while len(selected) < target_count and any(by_file.values()):
        for f in list(by_file.keys()):
            if by_file[f]:
                selected.append(by_file[f].pop(0))
                if len(selected) == target_count:
                    break

    return selected


def main():
    MUTANTS_DIR.mkdir(parents=True, exist_ok=True)
    candidates = find_mutation_candidates()
    print(f"Discovered {len(candidates)} total mutation candidates.")

    selected_candidates = select_diverse_mutants(candidates, target_count=40)
    print(f"Selected {len(selected_candidates)} diverse mutations across Flask.")

    mutants_index = []

    for i, (file_rel, line_no, old_line, new_line, desc) in enumerate(selected_candidates, 1):
        mid = f"m{i:02d}"
        diff_text = generate_diff(file_rel, line_no, old_line, new_line)

        diff_file = MUTANTS_DIR / f"{mid}.diff"
        diff_file.write_text(diff_text, encoding="utf-8")

        mutants_index.append({
            "id": mid,
            "description": desc,
            "file": file_rel,
            "line": line_no,
            "diff_file": str(diff_file.relative_to(Path("."))),
        })

    # Save index.json
    with open(MUTANTS_DIR / "index.json", "w", encoding="utf-8") as f:
        json.dump(mutants_index, f, indent=2)

    # Generate deterministic split using sha256 hash of mutant_id
    # Rule R3 Goodhart: Frozen file written BEFORE any tuning
    calibration = []
    held_out = []

    for m in mutants_index:
        mid = m["id"]
        # Hash to number 0-99
        h = int(hashlib.sha256(mid.encode("utf-8")).hexdigest(), 16) % 100
        if h < 40:
            calibration.append(mid)
        else:
            held_out.append(mid)

    split_data = {
        "description": "Deterministic split of 40 mutants: ~40% calibration, ~60% held-out. Frozen before tuning.",
        "calibration": sorted(calibration),
        "held_out": sorted(held_out),
    }

    with open(SPLIT_FILE, "w", encoding="utf-8") as f:
        json.dump(split_data, f, indent=2)

    print(f"Generated {len(mutants_index)} mutants in {MUTANTS_DIR}")
    print(f"Saved frozen split in {SPLIT_FILE}:")
    print(f"  Calibration: {len(calibration)} ({len(calibration)/len(mutants_index)*100:.1f}%)")
    print(f"  Held-out:    {len(held_out)} ({len(held_out)/len(mutants_index)*100:.1f}%)")


if __name__ == "__main__":
    main()
