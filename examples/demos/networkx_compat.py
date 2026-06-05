import streamlit as st
import networkx as nx
from streamlit_cytoscape import streamlit_cytoscape

st.markdown("# NetworkX Integration")
st.markdown("""
    Pass a NetworkX graph directly using `nx.cytoscape_data()`.
    Edge `source`/`target` types and missing edge `id` fields are
    automatically sanitized.
    """)

graph_type = st.selectbox(
    "Graph type",
    ["Karate Club", "Path", "Complete", "Petersen"],
)

if graph_type == "Karate Club":
    G = nx.karate_club_graph()
elif graph_type == "Path":
    G = nx.path_graph(8)
elif graph_type == "Complete":
    G = nx.complete_graph(6)
else:
    G = nx.petersen_graph()

cyto_data = nx.cytoscape_data(G)

st.caption(f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

streamlit_cytoscape(
    elements=cyto_data["elements"],
    layout="cose",
    height=500,
    key="networkx_compat",
)

with st.expander("Snippet", expanded=False, icon="\U0001f4bb"):
    st.code(
        """
        import networkx as nx
        from streamlit_cytoscape import streamlit_cytoscape

        G = nx.karate_club_graph()
        cyto_data = nx.cytoscape_data(G)

        streamlit_cytoscape(
            elements=cyto_data["elements"],
            layout="cose",
        )
    """,
        language="python",
    )
