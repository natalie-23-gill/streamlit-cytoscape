# Changelog

## v0.1.4 (01/08/2026)

### Bug Fixes
- Fixed meta-edge color persistence issue where meta-edges would remain red after deselection
- Meta-edges now preserve the color of their priority edge

### Improvements
- Added meta-edge style customization to edge_actions demo

## v0.1.3 (06/01/2026)

### Edge Actions: Collapse/Expand Parallel Edges
- Added `edge_actions` parameter to enable collapsing and expanding of parallel edges
- Parallel edges (multiple edges between the same source and target) can be collapsed into a single "meta-edge"
- Meta-edges display a priority label and the count of collapsed edges (e.g., "FOLLOWS (3)")
- Double-click a collapsed meta-edge to expand it back to individual edges
- New parameters:
  - `edge_actions`: List of actions to enable (`['collapse', 'expand']`)
  - `collapse_parallel_edges`: Auto-collapse parallel edges on initial render
  - `priority_edge_label`: Configure which edge label takes precedence on meta-edges
  - `meta_edge_style`: Dictionary of Cytoscape.js styles for customizing meta-edge appearance

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