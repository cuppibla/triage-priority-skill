#!/usr/bin/env python3
"""Install the pr-review skill into an explicitly selected project or user scope."""
import argparse
from pathlib import Path
import shutil
import sys

NAMES = ("pr-review",)


def snapshot(directory):
    if not directory.is_dir() or directory.is_symlink():
        return None
    result = {}
    for path in directory.rglob("*"):
        if path.is_symlink():
            return None
        if path.is_file():
            result[str(path.relative_to(directory))] = path.read_bytes()
    return result


def install(source, target):
    # Validate the skill and destination before writing.
    pending = []
    for name in NAMES:
        src, dst = source / name, target / name
        if not (src / "SKILL.md").is_file():
            raise ValueError(f"Missing source skill: {src / 'SKILL.md'}")
        contents = snapshot(src)
        if contents is None:
            raise ValueError(f"Source must contain ordinary files, not symlinks: {src}")
        if dst.exists() or dst.is_symlink():
            if snapshot(dst) != contents:
                raise ValueError(f"Existing skill differs; preserved without changes: {dst}\n"
                                 "Compare or back up that folder before installing this version.")
        else:
            pending.append((src, dst))
    if pending:
        target.mkdir(parents=True, exist_ok=True)
        for src, dst in pending:
            shutil.copytree(src, dst)
    for name in NAMES:
        print(f"Ready: {target / name / 'SKILL.md'}")
    print("In Claude Code, run /reload-skills, or restart Claude from the project you are reviewing.")
    print("Then use: /pr-review review #42")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Existing project directory to install into")
    scope.add_argument("--user", action="store_true", help="Install pr-review in ~/.claude/skills for all local projects")
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parent
    if args.user:
        target = Path.home() / ".claude" / "skills"
    else:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            parser.error(f"Project directory does not exist: {project}")
        target = project / ".claude" / "skills"
    try:
        install(source, target)
    except (OSError, ValueError) as exc:
        print(f"Install failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
