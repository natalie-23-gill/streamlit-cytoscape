"""
Simple example of st-cytoscape usage
"""

import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle, EdgeStyle, create_node, create_edge

st.title("Simple st-cytoscape Example")

# Create a simple social network
elements = [
    create_node("alice", "Alice", "person"),
    create_node("bob", "Bob", "person"),
    create_node("carol", "Carol", "person"),
    create_edge("e1", "alice", "bob", "friends", "friends"),
    create_edge("e2", "bob", "carol", "friends", "friends"),
]

# Define styles
node_styles = [NodeStyle("person", "#3498db", "label", "person", size=50)]

edge_styles = [EdgeStyle("friends", "#95a5a6", "label", directed=False, width=3)]

# Render the graph
event = st_cytoscape(
    elements=elements,
    node_styles=node_styles,
    edge_styles=edge_styles,
    layout="cose",
    height=400,
    key="simple_graph",
)

# Display events
if event:
    st.write(f"Event type: {event.get('type')}")
    if event.get("target"):
        st.write(f"Target: {event['target']}")
