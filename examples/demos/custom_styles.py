import json
import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle

with open("./data/social.json", "r") as f:
    elements = json.load(f)

st.markdown("# Custom Styles")
st.markdown(
    """
    The `custom_styles` parameter allows you to apply any valid Cytoscape.js style
    property to nodes and edges. This gives you fine-grained control over the
    appearance of your graph elements beyond the basic options.

    See the [Cytoscape.js style documentation](https://js.cytoscape.org/#style)
    for all available properties.
    """
)

st.markdown("## Node Custom Styles")

row1_left, row1_middle, row1_right = st.columns(3)
node_shape = row1_left.selectbox(
    "Shape",
    [
        "ellipse",
        "triangle",
        "rectangle",
        "diamond",
        "pentagon",
        "hexagon",
        "octagon",
        "star",
    ],
    index=0,
)
node_width = row1_middle.slider("Width", 20, 100, 50)
node_height = row1_right.slider("Height", 20, 100, 50)

row2_left, row2_middle, row2_right = st.columns(3)
node_border_width = row2_left.slider("Border Width", 0, 10, 3)
node_border_color = row2_middle.color_picker("Border Color", value="#000000")
node_border_style = row2_right.selectbox(
    "Border Style", ["solid", "dashed", "dotted", "double"], index=0
)

row3_left, row3_middle, row3_right = st.columns(3)
node_opacity = row3_left.slider("Node Opacity", 0.0, 1.0, 1.0, step=0.1)
label_font_size = row3_middle.slider("Label Font Size", 8, 24, 12)
label_color = row3_right.color_picker("Label Color", value="#FFFFFF")

st.markdown("## Edge Custom Styles")

row4_left, row4_middle, row4_right = st.columns(3)
edge_width = row4_left.slider("Edge Width", 1, 10, 2)
edge_style = row4_middle.selectbox("Line Style", ["solid", "dashed", "dotted"], index=0)
edge_opacity = row4_right.slider("Edge Opacity", 0.0, 1.0, 1.0, step=0.1)

row5_left, row5_middle, row5_right = st.columns(3)
arrow_shape = row5_left.selectbox(
    "Arrow Shape",
    [
        "triangle",
        "triangle-tee",
        "circle-triangle",
        "triangle-backcurve",
        "vee",
        "tee",
        "circle",
        "diamond",
        "chevron",
        "none",
    ],
    index=0,
)
arrow_scale = row5_middle.slider("Arrow Scale", 0.5, 3.0, 1.0, step=0.1)
edge_label_font_size = row5_right.slider("Edge Label Font Size", 8, 20, 10)

node_styles = [
    NodeStyle(
        label="PERSON",
        color="#FF7F3E",
        caption="name",
        icon="person",
        custom_styles={
            "shape": node_shape,
            "width": node_width,
            "height": node_height,
            "border-width": node_border_width,
            "border-color": node_border_color,
            "border-style": node_border_style,
            "opacity": node_opacity,
            "font-size": label_font_size,
            "color": label_color,
        },
    ),
    NodeStyle("POST", "#2A629A", "created_at", "description"),
]

edge_styles = [
    EdgeStyle(
        label="FOLLOWS",
        caption="label",
        directed=True,
        custom_styles={
            "width": edge_width,
            "line-style": edge_style,
            "opacity": edge_opacity,
            "target-arrow-shape": arrow_shape,
            "arrow-scale": arrow_scale,
            "font-size": edge_label_font_size,
        },
    ),
    EdgeStyle("POSTED", caption="label", directed=True),
    EdgeStyle("QUOTES", caption="label", directed=True),
]

layout = {"name": "cose", "animate": "end", "nodeDimensionsIncludeLabels": False}

st_cytoscape(
    elements,
    node_styles=node_styles,
    edge_styles=edge_styles,
    layout=layout,
    key="custom",
)

with st.expander("Snippet", expanded=False, icon="💻"):
    st.code(
        f"""
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle

node_styles = [
    NodeStyle(
        label="PERSON",
        color="#FF7F3E",
        caption="name",
        icon="person",
        custom_styles={{
            "shape": "{node_shape}",
            "width": {node_width},
            "height": {node_height},
            "border-width": {node_border_width},
            "border-color": "{node_border_color}",
            "border-style": "{node_border_style}",
            "opacity": {node_opacity},
            "font-size": {label_font_size},
            "color": "{label_color}",
        }},
    ),
    NodeStyle("POST", "#2A629A", "created_at", "description"),
]

edge_styles = [
    EdgeStyle(
        label="FOLLOWS",
        caption="label",
        directed=True,
        custom_styles={{
            "width": {edge_width},
            "line-style": "{edge_style}",
            "opacity": {edge_opacity},
            "target-arrow-shape": "{arrow_shape}",
            "arrow-scale": {arrow_scale},
            "font-size": {edge_label_font_size},
        }},
    ),
    EdgeStyle("POSTED", caption="label", directed=True),
    EdgeStyle("QUOTES", caption="label", directed=True),
]

layout = {{"name": "cose", "animate": "end", "nodeDimensionsIncludeLabels": False}}

elements = {json.dumps(elements)}

st_cytoscape(elements, node_styles=node_styles, edge_styles=edge_styles, layout=layout)
        """,
        language="python",
    )
