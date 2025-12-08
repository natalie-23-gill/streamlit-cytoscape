import json
import streamlit as st
from streamlit_cytoscape import streamlit_cytoscape, NodeStyle, EdgeStyle
from streamlit_cytoscape.icons import SUPPORTED_ICONS

with open("./data/social.json", "r") as f:
    elements = json.load(f)

PERSON_ATTRS = list(elements["nodes"][0]["data"].keys()) + [None]

st.markdown("# Node Styles")
st.markdown(
    """
    A unique node style can be applied to each group of nodes (grouped by
    `label`
    data element). Here is an example of modifying `PERSON` nodes styles
    """
)

left, middle, right = st.columns(3)
label = "PERSON"
icon = left.selectbox("Icon", SUPPORTED_ICONS, index=2)
caption = middle.selectbox("Caption", PERSON_ATTRS, index=3)
color = right.color_picker("Color", value="#FF7F3E")

node_styles = [
    NodeStyle(label, color, caption, icon),
    NodeStyle("POST", "#2A629A", "created_at", "description"),
]

edge_styles = [
    EdgeStyle("FOLLOWS", caption="label", directed=True),
    EdgeStyle("POSTED", caption="label", directed=True),
    EdgeStyle("QUOTES", caption="label", directed=True),
]

layout = {
    "name": "cose",
    "animate": "end",
    "nodeDimensionsIncludeLabels": False
}

streamlit_cytoscape(
    elements,
    node_styles=node_styles,
    edge_styles=edge_styles,
    layout=layout,
    key="xyz"
)

with st.expander("Snippet", expanded=False, icon="💻"):
    st.code(
        f"""
        from streamlit_cytoscape import streamlit_cytoscape, NodeStyle, EdgeStyle

        node_styles = [
            NodeStyle({label=}, {color=}, {caption=}, {icon=}),
            NodeStyle(
                label="POST", color="#2A629A",
                caption="created_at", icon="description"
            )
        ]

        edge_styles = [
            EdgeStyle("FOLLOWS", caption='label', directed=True),
            EdgeStyle("POSTED", caption='label', directed=True),
            EdgeStyle("QUOTES", caption='label', directed=True),
        ]

        layout = {{
            "name": "cose",
            "animate": "end",
            "nodeDimensionsIncludeLabels": False
        }}

        elements = {json.dumps(elements)}

        streamlit_cytoscape(elements, layout, node_styles, edge_styles, key="xyz")
    """,
        language="python",
    )
