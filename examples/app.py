import streamlit as st

st.set_page_config(layout="wide")

# -------- Examples / Demos --------
node_style = st.Page(
    "./demos/node_style.py",
    title="Node Styles",
    default=True,
)
edge_style = st.Page(
    "./demos/edge_style.py",
    title="Edge Styles",
)
custom_styles = st.Page(
    "./demos/custom_styles.py",
    title="Custom Styles",
)
layout = st.Page(
    "./demos/layout.py",
    title="Layout Algorithms",
)
event_listeners = st.Page(
    "./demos/event_listeners.py",
    title="Events Listeners",
)
node_actions = st.Page(
    "./demos/node_actions.py",
    title="Node Actions",
)
multi_tab = st.Page(
    "./demos/multi_tab.py",
    title="Multi-Tab",
)

# --------- Navigation ---------
pg = st.navigation([node_style, edge_style, custom_styles, layout, event_listeners, node_actions, multi_tab])
pg.run()
