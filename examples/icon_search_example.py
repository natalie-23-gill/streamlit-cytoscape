"""
Example demonstrating Material Icons API integration

This example shows how to:
1. Search for available Material Icons
2. Validate icon names
3. Use the icon API to dynamically select icons
"""

import streamlit as st
from st_cytoscape import st_cytoscape, NodeStyle, icons

st.set_page_config(page_title="Material Icons API Demo", layout="wide")

st.title("Material Icons API Demo")
st.markdown(
    """
This demo shows how st-cytoscape integrates with the Google Material Icons API
to provide icon validation and search capabilities.
"""
)

# Create two columns for the demo
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Icon Search")

    # Icon search functionality
    search_query = st.text_input(
        "Search for icons",
        placeholder="e.g., person, home, settings",
        help="Search for Material Icons by name",
    )

    if search_query:
        matching_icons = icons.search_icons(search_query)

        if matching_icons:
            st.success(f"Found {len(matching_icons)} matching icons")

            # Show first 20 matches
            st.markdown("**Matching icons (showing first 20):**")
            for icon in matching_icons[:20]:
                st.code(icon)
        else:
            st.warning("No matching icons found")

    st.divider()

    st.subheader("Icon Validation")

    # Icon validation
    icon_to_validate = st.text_input(
        "Validate an icon",
        placeholder="e.g., person",
        help="Check if an icon name is valid",
    )

    if icon_to_validate:
        is_valid = icons.is_valid_icon(icon_to_validate)

        if is_valid:
            st.success(f"✓ '{icon_to_validate}' is a valid Material Icon")
        else:
            st.error(f"✗ '{icon_to_validate}' is not a valid Material Icon")

            # Suggest similar icons
            suggestions = icons.search_icons(icon_to_validate)
            if suggestions:
                st.info(f"Did you mean one of these? {', '.join(suggestions[:5])}")

    st.divider()

    # Refresh icons button
    if st.button("Refresh Icon List from API"):
        with st.spinner("Fetching latest icons from Google..."):
            try:
                refreshed_icons = icons.refresh_icons()
                st.success(
                    f"Successfully loaded {len(refreshed_icons)} icons from Google Material Icons API"
                )
            except Exception as e:
                st.error(f"Failed to refresh icons: {e}")

with col2:
    st.subheader("Interactive Graph with Material Icons")

    # Let user select icons for different node types
    st.markdown("**Customize node icons:**")

    icon_col1, icon_col2, icon_col3 = st.columns(3)

    with icon_col1:
        person_icon = st.text_input("Person icon", value="person")

    with icon_col2:
        project_icon = st.text_input("Project icon", value="folder")

    with icon_col3:
        team_icon = st.text_input("Team icon", value="groups")

    # Create graph elements
    elements = [
        # Nodes
        {"data": {"id": "p1", "label": "Alice", "type": "person"}},
        {"data": {"id": "p2", "label": "Bob", "type": "person"}},
        {"data": {"id": "proj1", "label": "Project X", "type": "project"}},
        {"data": {"id": "team1", "label": "Dev Team", "type": "team"}},
        # Edges
        {"data": {"id": "e1", "source": "p1", "target": "proj1", "type": "works_on"}},
        {"data": {"id": "e2", "source": "p2", "target": "proj1", "type": "works_on"}},
        {"data": {"id": "e3", "source": "p1", "target": "team1", "type": "member_of"}},
        {"data": {"id": "e4", "source": "p2", "target": "team1", "type": "member_of"}},
    ]

    # Define node styles with user-selected icons
    # Note: Icon validation is enabled by default, so warnings will appear for invalid icons
    node_styles = [
        NodeStyle("person", "#3498db", "label", person_icon, size=50),
        NodeStyle("project", "#e74c3c", "label", project_icon, size=60),
        NodeStyle("team", "#2ecc71", "label", team_icon, size=55),
    ]

    # Render the graph
    st_cytoscape(
        elements=elements,
        node_styles=node_styles,
        layout="circle",
        height=400,
    )

    st.markdown(
        """
    **Note:** If you enter an invalid icon name, you'll see a warning in the console.
    The icon validation feature helps catch typos and ensures you're using valid Material Icons.
    """
    )

# Sidebar with additional information
with st.sidebar:
    st.subheader("About Material Icons API")

    st.markdown(
        """
    The Material Icons API integration provides:

    - **Automatic validation**: Icon names are validated against Google's Material Icons
    - **Smart caching**: Icons are cached locally to reduce API calls
    - **Search functionality**: Find icons by searching for keywords
    - **Error prevention**: Get warnings about invalid icon names

    ### API Functions

    ```python
    # Search for icons
    icons.search_icons("person")

    # Validate an icon
    icons.is_valid_icon("person")

    # Get all available icons
    icons.get_available_icons()

    # Refresh from API
    icons.refresh_icons()
    ```

    ### Using with NodeStyle

    ```python
    # Validation enabled (default)
    NodeStyle("person", "#3498db", icon="person")

    # Disable validation
    NodeStyle("person", "#3498db",
              icon="custom_icon",
              validate_icon=False)
    ```
    """
    )

    st.divider()

    # Show some statistics
    try:
        total_icons = len(icons.get_available_icons())
        st.metric("Total Material Icons Available", total_icons)
    except Exception:
        st.info("Icon count unavailable")
