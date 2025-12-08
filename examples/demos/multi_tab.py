"""
Demo to show the multi-tab auto-fit fix (st-link-analysis#35).

This creates two tabs with graphs to verify that:
1. Graph in first tab fits correctly on load
2. Graph in second tab auto-fits when tab becomes visible
"""

import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle

st.markdown("# Multi-Tab Auto-Fit Test")
st.markdown(
    """
    Multiple tabs with components get resized automatically to fit the graph
    when that tab is clicked.

    **Steps:**
    1. Observe that the graph in Tab 1 fits correctly
    2. Click on Tab 2 - the graph should auto-fit when the tab becomes visible
    3. Switch back to Tab 1 - it should still display correctly
    """
)

# Sample elements for testing
elements_tab1 = {
    "nodes": [
        {"data": {"id": "a", "label": "PERSON"}},
        {"data": {"id": "b", "label": "PERSON"}},
        {"data": {"id": "c", "label": "PERSON"}},
        {"data": {"id": "d", "label": "CAR"}},
        {"data": {"id": "e", "label": "CAR"}},
    ],
    "edges": [
        {"data": {"id": "ab", "source": "a", "target": "b", "label": "KNOWS"}},
        {"data": {"id": "bc", "source": "b", "target": "c", "label": "KNOWS"}},
        {"data": {"id": "ad", "source": "a", "target": "d", "label": "DRIVES"}},
        {"data": {"id": "ce", "source": "c", "target": "e", "label": "DRIVES"}},
    ],
}

elements_tab2 = {
    "nodes": [
        {"data": {"id": "n1", "label": "CLAIM"}},
        {"data": {"id": "n2", "label": "CLAIM"}},
        {"data": {"id": "n3", "label": "PERSON"}},
        {"data": {"id": "n4", "label": "CAR"}},
        {"data": {"id": "n5", "label": "CAR"}},
        {"data": {"id": "n6", "label": "PERSON"}},
    ],
    "edges": [
        {"data": {"id": "e1", "source": "n1", "target": "n3", "label": "FILED_BY"}},
        {"data": {"id": "e2", "source": "n2", "target": "n6", "label": "FILED_BY"}},
        {"data": {"id": "e3", "source": "n3", "target": "n4", "label": "DRIVES"}},
        {"data": {"id": "e4", "source": "n6", "target": "n5", "label": "DRIVES"}},
        {"data": {"id": "e5", "source": "n4", "target": "n1", "label": "INVOLVED_IN"}},
        {"data": {"id": "e6", "source": "n5", "target": "n2", "label": "INVOLVED_IN"}},
    ],
}

node_styles = [
    NodeStyle("PERSON", "#01204E", None, "person"),
    NodeStyle("CAR", "#028391", None, "directions_car"),
    NodeStyle("CLAIM", "#a87c2a", None, "description"),
]

tab1, tab2 = st.tabs(["Tab 1 - Graph A", "Tab 2 - Graph B"])

with tab1:
    st.markdown("### Graph A (loaded on page load)")
    st_cytoscape(elements_tab1, "fcose", node_styles, key="graph_tab1")

with tab2:
    st.markdown("### Graph B (should auto-fit when tab becomes visible)")
    st_cytoscape(elements_tab2, "fcose", node_styles, key="graph_tab2")
