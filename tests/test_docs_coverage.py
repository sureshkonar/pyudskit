import ast
from pathlib import Path


def _methods(path: str, class_name: str) -> set[str]:
    tree = ast.parse(Path(path).read_text())
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")}
    return set()


def test_docs_cover_all_methods():
    uds_methods = _methods("pyudskit/client.py", "UDS")
    ai_methods = _methods("pyudskit/ai/client.py", "AIClient")

    uds_doc = Path("docs/api-reference/uds-class.md").read_text()
    ai_doc = Path("docs/api-reference/ai-client.md").read_text()

    missing_uds = sorted(m for m in uds_methods if m not in uds_doc)
    missing_ai = sorted(m for m in ai_methods if m not in ai_doc)

    assert not missing_uds, f"UDS methods missing in docs: {missing_uds}"
    assert not missing_ai, f"AIClient methods missing in docs: {missing_ai}"
