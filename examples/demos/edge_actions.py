import streamlit as st
from streamlit_cytoscape import streamlit_cytoscape, NodeStyle, EdgeStyle
from streamlit_cytoscape.layouts import LAYOUTS

LAYOUT_NAMES = list(LAYOUTS.keys())

st.markdown("# Collapse / Expand Parallel Edges")
st.markdown(
    """
    The `edge_actions` parameter enables collapsing and expanding of parallel
    edges (multiple edges between the same source and target nodes). When
    parallel edges are collapsed, they appear as a single "meta-edge" showing:

    - A priority label (configurable via `priority_edge_label`)
    - The count of collapsed edges in parentheses

    Key features:
    - **Auto-collapse**: Set `collapse_parallel_edges=True` to collapse
    - **Expand on double-click**: Double-click a collapsed edge to expand
    - **Priority label**: Configure which edge label takes precedence

    #### Example use with a callback
    """
)

st.code(
    """
    def my_callback() -> None:
        val = st.session_state["mygraph"]
        if val["action"] == "expand_edge":
            group_key = val["data"]["group_key"]
            edge_count = val["data"]["edge_count"]
            # Handle edge expansion - e.g., update state or log

    streamlit_cytoscape(
        elements,
        edge_actions=['collapse', 'expand'],
        collapse_parallel_edges=True,
        priority_edge_label="FOLLOWS",  # Optional: which label shows on top
        on_change=my_callback,
        key="mygraph"
    )
    """,
    language="python",
)

st.info(
    """
    **Notes**
    - Collapsed edges are managed entirely in the frontend
    - Expanding sends an event to Python and restores edges in frontend
    - The meta-edge uses dashed styling to distinguish from regular edges
    """
)


def create_multi_edge_graph():
    """Create a graph with multiple parallel edges."""
    nodes = [
        {"data": {"id": "alice", "label": "PERSON", "name": "Alice"}},
        {"data": {"id": "bob", "label": "PERSON", "name": "Bob"}},
        {"data": {"id": "charlie", "label": "PERSON", "name": "Charlie"}},
        {"data": {"id": "diana", "label": "PERSON", "name": "Diana"}},
    ]

    # Multiple edges between same nodes (parallel edges)
    edges = [
        # Alice -> Bob (3 parallel edges)
        {
            "data": {
                "id": "e1",
                "label": "FOLLOWS",
                "source": "alice",
                "target": "bob",
                "since": "2020",
            }
        },
        {
            "data": {
                "id": "e2",
                "label": "LIKES",
                "source": "alice",
                "target": "bob",
                "since": "2021",
            }
        },
        {
            "data": {
                "id": "e3",
                "label": "WORKS_WITH",
                "source": "alice",
                "target": "bob",
                "since": "2022",
            }
        },
        # Bob -> Charlie (2 parallel edges)
        {
            "data": {
                "id": "e4",
                "label": "FOLLOWS",
                "source": "bob",
                "target": "charlie",
                "since": "2021",
            }
        },
        {
            "data": {
                "id": "e5",
                "label": "KNOWS",
                "source": "bob",
                "target": "charlie",
                "since": "2019",
            }
        },
        # Charlie -> Diana (1 edge - no parallel)
        {
            "data": {
                "id": "e6",
                "label": "FOLLOWS",
                "source": "charlie",
                "target": "diana",
                "since": "2023",
            }
        },
        # Diana -> Alice (2 parallel edges)
        {
            "data": {
                "id": "e7",
                "label": "FOLLOWS",
                "source": "diana",
                "target": "alice",
                "since": "2022",
            }
        },
        {
            "data": {
                "id": "e8",
                "label": "MENTORS",
                "source": "diana",
                "target": "alice",
                "since": "2021",
            }
        },
    ]

    return {"nodes": nodes, "edges": edges}


COMPONENT_KEY = "EDGE_ACTIONS"

# Create session state for elements if not exists
if "edge_graph" not in st.session_state:
    st.session_state.edge_graph = create_multi_edge_graph()

# Configuration options
col1, col2 = st.columns(2)
with col1:
    layout = st.selectbox("Layout", LAYOUT_NAMES, index=0)
    collapse_on_load = st.checkbox("Auto-collapse parallel edges", value=True)

with col2:
    priority_options = [None, "FOLLOWS", "LIKES", "WORKS_WITH", "KNOWS", "MENTORS"]
    priority_label = st.selectbox(
        "Priority edge label",
        priority_options,
        index=1,
        help="Which edge label should appear on top of collapsed edges",
    )

node_styles = [
    NodeStyle("PERSON", "#FF7F3E", "name", "person"),
]

edge_styles = [
    EdgeStyle("FOLLOWS", color="#2A629A", caption="label", directed=True),
    EdgeStyle("LIKES", color="#E74C3C", caption="label", directed=True),
    EdgeStyle("WORKS_WITH", color="#27AE60", caption="label", directed=True),
    EdgeStyle("KNOWS", color="#9B59B6", caption="label", directed=True),
    EdgeStyle("MENTORS", color="#F39C12", caption="label", directed=True),
]

# Meta-edge style customization (for testing)
meta_edge_style = {
    "line-style": "dashed",
    "width": 4,
    "font-weight": "bold",
}


def onchange_callback():
    """Handle edge action events from the component."""
    for key in st.session_state:
        if key.startswith(COMPONENT_KEY):
            val = st.session_state[key]
            if val and val.get("action") == "expand_edge":
                st.toast(
                    f"Expanded edge group: {val['data']['group_key']} "
                    f"({val['data']['edge_count']} edges)"
                )
            break


# Use a dynamic key that changes when collapse setting changes
# This forces a remount when toggling, which resets the frontend state
component_key = f"{COMPONENT_KEY}_{collapse_on_load}_{priority_label}"

elements = st.session_state.edge_graph
with st.container(border=True):
    vals = streamlit_cytoscape(
        elements,
        layout=layout,
        node_styles=node_styles,
        edge_styles=edge_styles,
        key=component_key,
        edge_actions=["collapse", "expand"],
        collapse_parallel_edges=collapse_on_load,
        priority_edge_label=priority_label,
        meta_edge_style=meta_edge_style,
        on_change=onchange_callback,
    )
    st.markdown("#### Returned Value")
    st.json(vals or {}, expanded=True)


st.markdown("### Graph Data")
st.markdown(
    """
    This demo uses a social network with multiple relationship types.
    Notice how Alice -> Bob has 3 edges (FOLLOWS, LIKES, WORKS_WITH)
    which collapse into a single meta-edge.
    """
)

with st.expander("View Graph Data", expanded=False):
    st.json(elements)


@st.cache_data
def get_source():
    with open(__file__, "r") as f:
        source = f.read()
    return source


source = get_source()
with st.expander("Source", expanded=False, icon=":material/code:"):
    st.code(source, language="python")
