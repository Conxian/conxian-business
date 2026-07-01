#!/usr/bin/env python3
"""Knowledge Retention Validator."""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
def main():
    print("=== Knowledge Retention Validator ===")
    kg_path = REPO_ROOT / "conxian-business" / "BOS_KNOWLEDGE_GRAPH.md"
    if not kg_path.exists():
        print(f"❌ FAIL: BOS Knowledge Graph missing at {kg_path}")
        sys.exit(1)
    print(f"✅ Found BOS Knowledge Graph: {kg_path}")
    print("✅ Knowledge Retention Validator: PASSED")
    sys.exit(0)
if __name__ == "__main__":
    main()
