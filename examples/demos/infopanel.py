import streamlit as st
from streamlit_cytoscape import streamlit_cytoscape

st.markdown("# Infopanel")
st.markdown(
    """
    Test page for infopanel attribute filtering.
    Click on a node to see its attributes in the infopanel.
    """
)

# Elements with both regular and underscore-prefixed attributes
elements = {
    "nodes": [
        {
            "data": {
                "id": "node1",
                "label": "NODE",
                "name": "Test Node",
                "visible_attr": "shown",
                "_hidden_attr": "hidden",
                "_style_data": "internal",
            }
        },
    ],
    "edges": [],
}

hide_underscore = st.checkbox("Hide underscore attributes", value=True)

streamlit_cytoscape(
    elements,
    layout="grid",
    hide_underscore_attrs=hide_underscore,
    key="infopanel_test",
)
