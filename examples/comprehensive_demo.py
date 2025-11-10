"""
Comprehensive demo of st-cytoscape features

This example demonstrates:
- Custom styling with custom_styles parameter (PR #62)
- Node positioning with coordinates (Issue #44)
- Customizable highlight styles (Issue #63)
- Dynamic resizing in multi-tab scenarios (Issue #35)
"""

import streamlit as st
from st_cytoscape import (
    st_cytoscape,
    NodeStyle,
    EdgeStyle,
    HighlightStyle,
    create_node,
    create_edge,
)

st.set_page_config(page_title="st-cytoscape Demo", layout="wide")

st.title("🔗 st-cytoscape: Flexible Graph Visualization")

st.markdown(
    """
This component addresses key issues from st-link-analysis:
- ✅ **Custom Styling** (PR #62): Built-in support for custom cytoscape.js styles
- ✅ **Coordinate Positioning** (Issue #44): Position nodes with x/y coordinates
- ✅ **Custom Highlights** (Issue #63): Fully customizable highlight styles
- ✅ **Auto-Resize** (Issue #35): Works correctly in multi-tab scenarios
"""
)

# Create tabs to demonstrate multi-tab support (Issue #35)
tab1, tab2, tab3 = st.tabs(
    ["📊 Network Graph", "🎨 Custom Styling", "📍 Positioned Layout"]
)

with tab1:
    st.header("Interactive Network Graph")
    st.markdown("Demonstrates basic usage with automatic layout")

    # Create elements
    elements = [
        create_node("alice", "Alice", "person"),
        create_node("bob", "Bob", "person"),
        create_node("carol", "Carol", "person"),
        create_node("project1", "Project Alpha", "project"),
        create_node("project2", "Project Beta", "project"),
        create_edge("e1", "alice", "bob", "collaborates", "works with"),
        create_edge("e2", "bob", "carol", "collaborates", "works with"),
        create_edge("e3", "alice", "project1", "manages", "manages"),
        create_edge("e4", "bob", "project1", "contributes", "contributes to"),
        create_edge("e5", "carol", "project2", "manages", "manages"),
    ]

    # Define styles
    node_styles = [
        NodeStyle("person", "#3498db", "label", "person", size=50),
        NodeStyle("project", "#e74c3c", "label", "folder", size=60),
    ]

    edge_styles = [
        EdgeStyle("collaborates", "#95a5a6", "label", directed=False, width=3),
        EdgeStyle("manages", "#2ecc71", "label", directed=True, width=4),
        EdgeStyle("contributes", "#f39c12", "label", directed=True, width=2),
    ]

    # Custom highlight style (Issue #63)
    highlight = HighlightStyle(
        node_border_color="#FFD700",
        node_border_width=4,
        edge_color="#FF6347",
        edge_width=5,
    )

    event = st_cytoscape(
        elements=elements,
        node_styles=node_styles,
        edge_styles=edge_styles,
        layout="cose",
        height=500,
        selection_type="additive",
        highlight_style=highlight,
        auto_resize=True,  # Fix for Issue #35
        key="network_graph",
    )

    if event:
        st.write("**Last Event:**", event)

with tab2:
    st.header("Custom Styling Demonstration")
    st.markdown("Shows custom_styles support from PR #62")

    # Create elements with custom visual properties
    custom_elements = [
        create_node("n1", "Custom Shape", "custom1"),
        create_node("n2", "Custom Border", "custom2"),
        create_node("n3", "Custom Opacity", "custom3"),
        create_node("n4", "Custom Text", "custom4"),
        create_edge("ce1", "n1", "n2", "dashed"),
        create_edge("ce2", "n2", "n3", "dotted"),
        create_edge("ce3", "n3", "n4", "thick"),
    ]

    # Demonstrate custom_styles parameter (PR #62)
    custom_node_styles = [
        NodeStyle(
            "custom1",
            "#9b59b6",
            "label",
            size=60,
            custom_styles={
                "shape": "diamond",
                "background-opacity": 0.8,
            },
        ),
        NodeStyle(
            "custom2",
            "#1abc9c",
            "label",
            size=70,
            custom_styles={
                "shape": "hexagon",
                "border-width": 5,
                "border-color": "#34495e",
                "border-style": "double",
            },
        ),
        NodeStyle(
            "custom3",
            "#f1c40f",
            "label",
            size=80,
            custom_styles={
                "shape": "triangle",
                "background-opacity": 0.6,
            },
        ),
        NodeStyle(
            "custom4",
            "#e67e22",
            "label",
            size=50,
            custom_styles={
                "shape": "rectangle",
                "text-background-color": "#fff",
                "text-background-opacity": 0.9,
                "text-background-padding": "5px",
            },
        ),
    ]

    custom_edge_styles = [
        EdgeStyle(
            "dashed",
            "#8e44ad",
            width=3,
            custom_styles={"line-style": "dashed"},
        ),
        EdgeStyle(
            "dotted",
            "#16a085",
            width=4,
            custom_styles={"line-style": "dotted"},
        ),
        EdgeStyle(
            "thick",
            "#d35400",
            width=8,
            custom_styles={"curve-style": "bezier"},
        ),
    ]

    st_cytoscape(
        elements=custom_elements,
        node_styles=custom_node_styles,
        edge_styles=custom_edge_styles,
        layout="circle",
        height=500,
        key="custom_styling",
    )

    st.info("💡 Use `custom_styles` to pass any Cytoscape.js style property!")

with tab3:
    st.header("Coordinate-Based Positioning")
    st.markdown("Demonstrates Issue #44: Position nodes with exact coordinates")

    # Create positioned elements (Issue #44)
    positioned_elements = [
        create_node("center", "Center", "hub", x=0, y=0),
        create_node("north", "North", "satellite", x=0, y=-200),
        create_node("south", "South", "satellite", x=0, y=200),
        create_node("east", "East", "satellite", x=200, y=0),
        create_node("west", "West", "satellite", x=-200, y=0),
        create_edge("en1", "center", "north", "connects"),
        create_edge("es1", "center", "south", "connects"),
        create_edge("ee1", "center", "east", "connects"),
        create_edge("ew1", "center", "west", "connects"),
    ]

    positioned_node_styles = [
        NodeStyle("hub", "#e74c3c", "label", "hub", size=80),
        NodeStyle("satellite", "#3498db", "label", "location_on", size=50),
    ]

    positioned_edge_styles = [
        EdgeStyle("connects", "#95a5a6", directed=True, width=2),
    ]

    st_cytoscape(
        elements=positioned_elements,
        node_styles=positioned_node_styles,
        edge_styles=positioned_edge_styles,
        layout="preset",  # Use preset layout to honor positions
        height=500,
        key="positioned_graph",
    )

    st.success("✅ Nodes are positioned using exact x/y coordinates!")

# Sidebar with feature information
with st.sidebar:
    st.header("Features")

    st.subheader("✨ New in st-cytoscape")
    st.markdown(
        """
    **1. Custom Styling (PR #62)**
    ```python
    NodeStyle(
        "type",
        custom_styles={
            "shape": "diamond",
            "border-width": 5
        }
    )
    ```

    **2. Coordinate Positioning (Issue #44)**
    ```python
    create_node("id", "Label", "type", x=100, y=200)
    ```

    **3. Custom Highlights (Issue #63)**
    ```python
    HighlightStyle(
        node_border_color="#FFD700",
        edge_color="#FF6347"
    )
    ```

    **4. Auto-Resize (Issue #35)**
    - Works correctly in multi-tab scenarios
    - Automatically adjusts to container size
    """
    )

    st.subheader("📚 Supported Layouts")
    st.markdown(
        """
    - `cose` - Physics-based
    - `grid` - Grid layout
    - `circle` - Circular layout
    - `concentric` - Concentric circles
    - `breadthfirst` - Tree layout
    - `preset` - Use provided positions
    """
    )
