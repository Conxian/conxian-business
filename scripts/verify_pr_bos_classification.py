import json
import os
import re
import sys


CLASSIFICATION_LABELS = [
    "docs-only",
    "stub-isolation",
    "dev-only implementation",
    "production implementation",
]


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH not set; cannot validate PR classification")
        return 1

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    pr = event.get("pull_request")
    if not pr:
        print("No pull_request payload found; nothing to validate")
        return 0

    actor = (os.environ.get("GITHUB_ACTOR") or "").strip()
    pr_author = ((pr.get("user") or {}).get("login") or "").strip()
    if actor == "dependabot[bot]" or pr_author == "dependabot[bot]":
        print("Skipping BOS PR classification for dependabot")
        return 0

    body = pr.get("body") or ""

    lines = body.splitlines()
    section_start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "### bos change classification":
            section_start = i + 1
            break

    if section_start is None:
        section_lines: list[str] = []
    else:
        section_end = next(
            (
                j
                for j in range(section_start, len(lines))
                if lines[j].lstrip().startswith("### ")
            ),
            len(lines),
        )
        section_lines = lines[section_start:section_end]

    selected: list[str] = []
    checkbox_re = re.compile(r"^\s*-\s*\[[xX]\]\s*(.+?)\s*$")
    for line in section_lines:
        match = checkbox_re.match(line)
        if not match:
            continue
        label = match.group(1).strip().lower()
        if label in CLASSIFICATION_LABELS:
            selected.append(label)

    if len(selected) != 1:
        expected = ", ".join(CLASSIFICATION_LABELS)
        print("BOS PR classification is required.")
        print(f"Select exactly one of: {expected}")
        print(
            "Add a checked box to the PR description under the 'BOS change classification' section."
        )
        if selected:
            print(f"Found multiple classifications checked: {', '.join(selected)}")
        return 1

    print(f"BOS PR classification: OK ({selected[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
