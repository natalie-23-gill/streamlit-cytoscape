import copy
from typing import Dict, Any


def sanitize_elements(elements: Dict[str, Any]) -> Dict[str, Any]:
    """Return a sanitized deep copy of *elements* for Cytoscape.js.

    - Coerces node ``id`` values to strings.
    - Coerces edge ``source`` / ``target`` values to strings.
    - Assigns ``_auto_e{i}`` IDs to edges that lack an ``id``.
    - Never mutates the input dict.
    """
    elements = copy.deepcopy(elements)

    for node in elements.get("nodes", []):
        data = node.get("data", {})
        if "id" in data:
            data["id"] = str(data["id"])

    for i, edge in enumerate(elements.get("edges", [])):
        data = edge.get("data", {})
        if "id" not in data:
            data["id"] = f"_auto_e{i}"
        if "source" in data:
            data["source"] = str(data["source"])
        if "target" in data:
            data["target"] = str(data["target"])

    return elements
