# Changelog

<!--next-version-placeholder-->

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