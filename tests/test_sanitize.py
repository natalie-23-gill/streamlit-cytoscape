import json
import copy
import os

import pytest

from streamlit_cytoscape.sanitize import sanitize_elements

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "examples", "data")


def test_does_not_mutate_input():
    original = {
        "nodes": [{"data": {"id": 1}}],
        "edges": [{"data": {"source": 1, "target": 2}}],
    }
    snapshot = copy.deepcopy(original)
    sanitize_elements(original)
    assert original == snapshot


def test_node_ids_stringified():
    elements = {"nodes": [{"data": {"id": 42}}, {"data": {"id": 7}}]}
    result = sanitize_elements(elements)
    assert result["nodes"][0]["data"]["id"] == "42"
    assert result["nodes"][1]["data"]["id"] == "7"


def test_edge_source_target_stringified():
    elements = {
        "edges": [{"data": {"id": "e0", "source": 1, "target": 2}}],
    }
    result = sanitize_elements(elements)
    assert result["edges"][0]["data"]["source"] == "1"
    assert result["edges"][0]["data"]["target"] == "2"


def test_missing_edge_ids_auto_generated():
    elements = {
        "edges": [
            {"data": {"source": "a", "target": "b"}},
            {"data": {"source": "c", "target": "d"}},
        ],
    }
    result = sanitize_elements(elements)
    assert result["edges"][0]["data"]["id"] == "_auto_e0"
    assert result["edges"][1]["data"]["id"] == "_auto_e1"


def test_existing_edge_ids_preserved():
    elements = {
        "edges": [{"data": {"id": "my_edge", "source": "a", "target": "b"}}],
    }
    result = sanitize_elements(elements)
    assert result["edges"][0]["data"]["id"] == "my_edge"


def test_integer_ids_referential_integrity():
    """Edge source/target must match their node IDs after coercion."""
    elements = {
        "nodes": [{"data": {"id": 1}}, {"data": {"id": 2}}],
        "edges": [{"data": {"id": "e0", "source": 1, "target": 2}}],
    }
    result = sanitize_elements(elements)
    node_ids = {n["data"]["id"] for n in result["nodes"]}
    for edge in result["edges"]:
        assert edge["data"]["source"] in node_ids
        assert edge["data"]["target"] in node_ids


@pytest.mark.parametrize("elements", [{}, {"nodes": [], "edges": []}])
def test_empty_elements(elements):
    result = sanitize_elements(elements)
    assert isinstance(result, dict)


def test_well_formed_graph_unchanged():
    with open(os.path.join(DATA_DIR, "social.json")) as f:
        elements = json.load(f)
    result = sanitize_elements(elements)

    assert len(result["nodes"]) == len(elements["nodes"])
    assert len(result["edges"]) == len(elements["edges"])

    for orig, san in zip(elements["nodes"], result["nodes"]):
        assert orig["data"]["id"] == san["data"]["id"]
        assert set(orig["data"].keys()) == set(san["data"].keys())

    for orig, san in zip(elements["edges"], result["edges"]):
        assert orig["data"]["id"] == san["data"]["id"]
        assert set(orig["data"].keys()) == set(san["data"].keys())
