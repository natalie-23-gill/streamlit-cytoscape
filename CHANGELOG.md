# Changelog

## v0.1.2 (02/01/2026)

### Infopanel Attribute Filtering
- Added `hide_underscore_attrs` parameter to `streamlit_cytoscape()` function
- When enabled (default: `True`), element data attributes with keys starting with `_` are hidden from the infopanel
- Allows users to distinguish between user-facing data and internal styling/rendering data

## v0.1.1 (08/12/2025)

- Fixing missing frontend error

## v0.1.0 (08/12/2025)

- First release of `streamlit_cytoscape`!

### Custom Styling Support
- Added `custom_styles` parameter to `NodeStyle`, `EdgeStyle`, and `HighlightStyle` classes
- Allows pass-through of any Cytoscape.js style property (shape, border-width, line-style, etc.)
- Provides maximum flexibility without exposing every option explicitly

### Multi-Tab Resizing
- Implemented ResizeObserver-based auto-resize in the frontend
- Fixes visualization issues when switching between Streamlit tabs
- Graph now correctly resizes and renders when tab becomes visible