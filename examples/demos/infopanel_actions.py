import json
import copy
from datetime import datetime
import streamlit as st
from streamlit_cytoscape import (
    streamlit_cytoscape,
    NodeStyle,
    EdgeStyle,
    InfopanelAction,
)

with open("./data/social.json", "r") as f:
    base_elements = json.load(f)

st.markdown("# Infopanel Actions")
st.markdown(
    """
    The `infopanel_actions` parameter adds custom action buttons
    to the infopanel. When clicked, the action name and selected
    element data are sent back to the Streamlit app. The callback
    can then update the element data, and the infopanel will
    reflect the changes on re-render.

    **Try it:** Select a node, then click an action button. The
    infopanel will update to show new attributes added by the
    callback.
    """
)

st.code(
    """
    from streamlit_cytoscape import InfopanelAction

    actions = [
        InfopanelAction("ai_summary", "AI Summary", icon="science"),
        InfopanelAction("fetch_details", "Fetch Details", icon="analytics"),
        InfopanelAction("flag_review", "Flag for Review", icon="flag"),
    ]

    def on_action():
        val = st.session_state["my_graph"]
        action = val["action"]
        eid = val["data"]["element_id"]
        # Update the element data based on the action...

    streamlit_cytoscape(
        elements,
        infopanel_actions=actions,
        on_change=on_action,
        key="my_graph"
    )
    """,
    language="python",
)

COMPONENT_KEY = "infopanel_actions_demo"

# Store elements in session state so callbacks can modify them
if "ip_elements" not in st.session_state:
    st.session_state.ip_elements = copy.deepcopy(base_elements)

node_styles = [
    NodeStyle("PERSON", "#FF7F3E", "email", "person"),
    NodeStyle("POST", "#2A629A", "created_at", "description"),
]

edge_styles = [
    EdgeStyle("FOLLOWS", caption="label", directed=True),
    EdgeStyle("POSTED", caption="label", directed=True),
    EdgeStyle("QUOTES", caption="label", directed=True),
]

actions = [
    InfopanelAction("ai_summary", "AI Summary", icon="science"),
    InfopanelAction("fetch_details", "Fetch Details", icon="analytics"),
    InfopanelAction("flag_review", "Flag for Review", icon="flag"),
]


def _find_node(elements, node_id):
    for node in elements["nodes"]:
        if node["data"]["id"] == node_id:
            return node["data"]
    return None


def on_action():
    val = st.session_state[COMPONENT_KEY]
    if not val or "action" not in val:
        return
    action = val["action"]
    eid = val["data"]["element_id"]
    data = _find_node(st.session_state.ip_elements, eid)
    if data is None:
        return

    now = datetime.now().strftime("%H:%M:%S")
    if action == "ai_summary":
        name = data.get("name", data.get("content", eid))
        data["ai_summary"] = f"Summary of {name}"
        data["summary_at"] = now
    elif action == "fetch_details":
        data["fetched_at"] = now
        data["status"] = "details loaded"
    elif action == "flag_review":
        data["flagged"] = "yes"
        data["flagged_at"] = now


with st.container(border=True):
    vals = streamlit_cytoscape(
        st.session_state.ip_elements,
        layout="fcose",
        node_styles=node_styles,
        edge_styles=edge_styles,
        infopanel_actions=actions,
        on_change=on_action,
        key=COMPONENT_KEY,
    )
    st.markdown("#### Returned Value")
    st.json(vals or {}, expanded=True)

if vals and vals.get("action"):
    st.success(
        f"Action **{vals['action']}** triggered on "
        f"**{vals['data']['element_id']}**"
    )


@st.cache_data
def get_source():
    with open(__file__, "r") as f:
        source = f.read()
    return source


source = get_source()
with st.expander("Source", expanded=False, icon="💻"):
    st.code(source, language="python")
