import json
import copy
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
from streamlit_cytoscape import (
    streamlit_cytoscape,
    NodeStyle,
    EdgeStyle,
    InfopanelAction,
)

with open("./data/social.json", "r") as f:
    base_elements = json.load(f)

st.markdown("# Infopanel")
st.markdown("""
    The infopanel shows attributes of the selected element.
    Use `hide_underscore_attrs` to hide internal attributes
    prefixed with `_`. The `infopanel_actions` parameter adds
    custom action buttons. When clicked, the action name and
    selected element data are sent back to the Streamlit app.

    **Try it:** Select a node, then click an action button. The
    infopanel will update to show new attributes added by the
    callback. Toggle the checkbox to show/hide underscore
    attributes.

    **Non-blocking actions:** The **AI Summary** action runs a
    (simulated) slow API call in a background thread. Set
    `spinner=True` on the action for instant click feedback, kick
    the work off in `on_change`, and poll for the result with an
    `st.fragment(run_every=...)` - the graph stays interactive the
    whole time and the summary fills in when it is ready.
    """)

st.code(
    """
    from concurrent.futures import ThreadPoolExecutor
    from streamlit_cytoscape import InfopanelAction

    actions = [
        # spinner=True -> instant busy feedback for the async action
        InfopanelAction("ai_summary", "AI Summary",
                        icon="science", spinner=True),
        InfopanelAction("fetch_details", "Fetch Details", icon="analytics"),
        InfopanelAction("flag_review", "Flag for Review", icon="flag"),
    ]

    def on_action():
        val = st.session_state["my_graph"]
        eid = val["data"]["element_id"]
        if val["action"] == "ai_summary":
            # Start background work and return immediately (no freeze)
            set_pending(eid)
            st.session_state.futures[eid] = executor.submit(call_api, eid)

    @st.fragment(run_every=1.0)
    def poll():
        for eid, fut in list(st.session_state.futures.items()):
            if fut.done():
                write_result(eid, fut.result())
                del st.session_state.futures[eid]
                st.rerun(scope="app")
    """,
    language="python",
)

COMPONENT_KEY = "infopanel_actions_demo"

# Store elements in session state so callbacks can modify them
if "ip_elements" not in st.session_state:
    st.session_state.ip_elements = copy.deepcopy(base_elements)
    # Add underscore-prefixed attrs to first node for hide/show demo
    n0 = st.session_state.ip_elements["nodes"][0]["data"]
    n0["_style_data"] = "internal"
    n0["_hidden_attr"] = "hidden"

# Track in-flight background summary jobs per node id (Future objects).
if "summary_futures" not in st.session_state:
    st.session_state.summary_futures = {}


@st.cache_resource
def _summary_executor() -> ThreadPoolExecutor:
    """Shared pool that runs summary generation off-thread."""
    return ThreadPoolExecutor(max_workers=4)


def _generate_summary(name: str) -> str:
    """Simulate a slow AI/API call.

    Replace the body with a real blocking request (e.g. an LLM
    call). It runs in a worker thread, so the Streamlit app stays
    responsive. Do NOT touch st.session_state here - return the
    result and let the main thread read it via Future.result().
    """
    time.sleep(2)
    return f"AI summary for {name}: a concise, generated description."


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
    InfopanelAction("ai_summary", "AI Summary", icon="science", spinner=True),
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
        # Kick off the work in the background and return at once,
        # so the app does not freeze. Dedupe repeated clicks.
        if eid not in st.session_state.summary_futures:
            name = data.get("name", data.get("content", eid))
            data["ai_summary"] = "⏳ generating..."
            fut = _summary_executor().submit(_generate_summary, name)
            st.session_state.summary_futures[eid] = fut
    elif action == "fetch_details":
        data["fetched_at"] = now
        data["status"] = "details loaded"
    elif action == "flag_review":
        data["flagged"] = "yes"
        data["flagged_at"] = now


@st.fragment(run_every=1.0)
def poll_summaries():
    """Poll in-flight summaries: when a Future is done, write its
    result into the node data and trigger a full rerun so the
    infopanel updates in place (selection/collapse preserved by the
    component). Polling stops once nothing is pending."""
    futures = st.session_state.summary_futures
    done_ids = [eid for eid, fut in futures.items() if fut.done()]
    for eid in done_ids:
        node = _find_node(st.session_state.ip_elements, eid)
        if node is not None:
            node["ai_summary"] = futures[eid].result()
            node["summary_at"] = datetime.now().strftime("%H:%M:%S")
        del futures[eid]
    if done_ids:
        st.rerun(scope="app")


hide_underscore = st.checkbox("Hide underscore attributes", value=True)

with st.container(border=True):
    vals = streamlit_cytoscape(
        st.session_state.ip_elements,
        layout="fcose",
        node_styles=node_styles,
        edge_styles=edge_styles,
        infopanel_actions=actions,
        hide_underscore_attrs=hide_underscore,
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

# While a summary is running, poll for its result. The graph above
# stays fully interactive (pan / zoom / select) the whole time.
if st.session_state.summary_futures:
    poll_summaries()


@st.cache_data
def get_source():
    with open(__file__, "r") as f:
        source = f.read()
    return source


source = get_source()
with st.expander("Source", expanded=False, icon="💻"):
    st.code(source, language="python")
