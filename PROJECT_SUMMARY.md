# st-cytoscape Project Summary

## Overview

A Streamlit component for interactive graph visualization using Cytoscape.js, addressing limitations in [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis).

## Solutions

### Custom Styling (PR #62)
- `custom_styles` parameter in `NodeStyle` and `EdgeStyle`
- Pass any Cytoscape.js style property (shape, border-width, line-style, etc.)

### Coordinate Positioning (Issue #44)
- x/y coordinates in `create_node()` helper
- Use `layout="preset"` to honor positions

### Multi-Tab Resizing (Issue #35)
- ResizeObserver-based auto-resize
- Works correctly when switching Streamlit tabs

### Custom Highlights (Issue #63)
- `HighlightStyle` class for selection appearance
- Separate customization for nodes and edges

## Structure

```
st-cytoscape/
├── st_cytoscape/         # Python package (component, styles, events)
├── frontend/             # React/TypeScript component
├── examples/             # Demo applications
└── tests/                # Unit tests
```

## Key Features

**Python API:**
- `NodeStyle`, `EdgeStyle`, `HighlightStyle` with `custom_styles` support
- `create_node()`, `create_edge()` helpers
- Multiple layouts and interaction options

**Frontend:**
- Cytoscape.js integration with TypeScript
- ResizeObserver for auto-resize
- Material icon support

## Development

```bash
cd frontend && npm start
streamlit run examples/comprehensive_demo.py
```

Build: `cd frontend && npm run build`

## Testing

```bash
pytest tests/
```

## Philosophy

Minimal changes, maximum flexibility. Reuses proven patterns from st-link-analysis while addressing core customization needs through extensibility hooks (`custom_styles`) rather than exposing every option.
