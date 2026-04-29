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
    title="Custom CSS",
)
layout = st.Page(
    "./demos/layout.py",
    title="Layouts",
)
node_actions = st.Page(
    "./demos/node_actions.py",
    title="Expand & Remove",
)
edge_actions = st.Page(
    "./demos/edge_actions.py",
    title="Parallel Edges",
)
infopanel_actions = st.Page(
    "./demos/infopanel_actions.py",
    title="Infopanel",
)
multi_tab = st.Page(
    "./demos/multi_tab.py",
    title="Multi-Tab",
)
networkx_compat = st.Page(
    "./demos/networkx_compat.py",
    title="NetworkX",
)

# --------- Navigation ---------
pg = st.navigation(
    [
        node_style,
        edge_style,
        custom_styles,
        layout,
        node_actions,
        edge_actions,
        infopanel_actions,
        multi_tab,
        networkx_compat,
    ]
)
pg.run()
