from datetime import datetime
import streamlit as st
from streamlit_cytoscape import (
    streamlit_cytoscape,
    NodeStyle,
    EdgeStyle,
    InfopanelAction,
)

st.markdown("# Links & Updates")
st.markdown("""
    The infopanel renders `<a href="...">` values in element data as real
    clickable links (http/https only). Anchors are rebuilt via the DOM API,
    so no other HTML/attributes are executed - a value containing a
    `<script>` or `onerror` payload is shown as inert text.

    This page also shows that updating a node's data (the **Add Note**
    action) does **not** re-expand the collapsed parallel edges or move the
    nodes - the graph state is preserved across the update.
    """)


def build_graph():
    """Small social graph with parallel edges and link/HTML attrs."""
    nodes = [
        {
            "data": {
                "id": "alice",
                "label": "PERSON",
                "name": "Alice",
                # Rendered as a real clickable link in the infopanel.
                "publication": (
                    '<a href="https://pubmed.ncbi.nlm.nih.gov/12345">'
                    "PMID:12345</a>"
                ),
                # Must NOT execute - shown as inert text.
                "unsafe": ('<img src=x onerror="window.__xss_fired = true">'),
            }
        },
        {"data": {"id": "bob", "label": "PERSON", "name": "Bob"}},
        {"data": {"id": "charlie", "label": "PERSON", "name": "Charlie"}},
        {"data": {"id": "diana", "label": "PERSON", "name": "Diana"}},
    ]
    edges = [
        # alice -> bob (3 parallel edges -> one meta-edge)
        {
            "data": {
                "id": "e1",
                "label": "FOLLOWS",
                "source": "alice",
                "target": "bob",
            }
        },
        {
            "data": {
                "id": "e2",
                "label": "LIKES",
                "source": "alice",
                "target": "bob",
            }
        },
        {
            "data": {
                "id": "e3",
                "label": "WORKS_WITH",
                "source": "alice",
                "target": "bob",
            }
        },
        # bob -> charlie (2 parallel edges -> one meta-edge)
        {
            "data": {
                "id": "e4",
                "label": "FOLLOWS",
                "source": "bob",
                "target": "charlie",
            }
        },
        {
            "data": {
                "id": "e5",
                "label": "KNOWS",
                "source": "bob",
                "target": "charlie",
            }
        },
        # charlie -> diana (single edge)
        {
            "data": {
                "id": "e6",
                "label": "FOLLOWS",
                "source": "charlie",
                "target": "diana",
            }
        },
    ]
    return {"nodes": nodes, "edges": edges}


COMPONENT_KEY = "infopanel_links_demo"

if "links_elements" not in st.session_state:
    st.session_state.links_elements = build_graph()

node_styles = [NodeStyle("PERSON", "#FF7F3E", "name", "person")]
edge_styles = [
    EdgeStyle("FOLLOWS", color="#2A629A", caption="label", directed=True),
    EdgeStyle("LIKES", color="#E74C3C", caption="label", directed=True),
    EdgeStyle("WORKS_WITH", color="#27AE60", caption="label", directed=True),
    EdgeStyle("KNOWS", color="#9B59B6", caption="label", directed=True),
]

actions = [InfopanelAction("add_note", "Add Note", icon="flag")]


def _find_node(elements, node_id):
    for node in elements["nodes"]:
        if node["data"]["id"] == node_id:
            return node["data"]
    return None


def on_action():
    val = st.session_state[COMPONENT_KEY]
    if not val or val.get("action") != "add_note":
        return
    eid = val["data"]["element_id"]
    data = _find_node(st.session_state.links_elements, eid)
    if data is not None:
        # Plain node-data update: used to re-expand collapsed edges.
        data["note"] = f"updated at {datetime.now().strftime('%H:%M:%S')}"


with st.container(border=True):
    vals = streamlit_cytoscape(
        st.session_state.links_elements,
        layout="fcose",
        node_styles=node_styles,
        edge_styles=edge_styles,
        infopanel_actions=actions,
        edge_actions=["collapse", "expand"],
        collapse_parallel_edges=True,
        priority_edge_label="FOLLOWS",
        on_change=on_action,
        key=COMPONENT_KEY,
    )
    st.markdown("#### Returned Value")
    st.json(vals or {}, expanded=True)


@st.cache_data
def get_source():
    with open(__file__, "r") as f:
        return f.read()


with st.expander("Source", expanded=False, icon="💻"):
    st.code(get_source(), language="python")
