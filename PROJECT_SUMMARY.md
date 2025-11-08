# st-cytoscape Project Summary

## Overview

st-cytoscape is a flexible Streamlit component for interactive graph visualization using Cytoscape.js. It was created to address several unresolved issues and limitations in the [st-link-analysis](https://github.com/AlrasheedA/st-link-analysis) library.

## Problems Addressed

### 1. Custom Styling Support (PR #62)

**Original Issue:** [PR #62](https://github.com/AlrasheedA/st-link-analysis/pull/62) proposed adding a `custom_styles` parameter to allow passing arbitrary Cytoscape.js style properties, but remains unmerged.

**Our Solution:**
- Built-in `custom_styles` parameter in both `NodeStyle` and `EdgeStyle` classes
- Allows passing any Cytoscape.js style property (shape, border-width, line-style, etc.)
- Fully integrated into the styling system from day one

**Implementation:**
```python
# st_cytoscape/styles.py - NodeStyle and EdgeStyle classes
custom_styles: Optional[Dict[str, Any]] = None

# frontend/src/StCytoscapeComponent.tsx - Applied in buildCytoscapeStyles()
...style.custom_styles  // Spread operator merges custom styles
```

### 2. Node Positioning with Coordinates (Issue #44)

**Original Issue:** [Issue #44](https://github.com/AlrasheedA/st-link-analysis/issues/44) requested the ability to position nodes using exact x/y coordinates.

**Our Solution:**
- Support for x/y coordinates in `create_node()` helper function
- Position parameter in `NodeStyle` for default positioning by type
- Automatic coordinate handling in the component
- Use `layout="preset"` to honor provided positions

**Implementation:**
```python
# st_cytoscape/component.py - create_node()
def create_node(id, label, node_type, x=None, y=None, **additional_data):
    if x is not None and y is not None:
        node["position"] = {"x": x, "y": y}

# Component processes positions from multiple sources
```

### 3. Dynamic Resizing in Multi-Tab Scenarios (Issue #35)

**Original Issue:** [Issue #35](https://github.com/AlrasheedA/st-link-analysis/issues/35) reported that graphs don't automatically fit to screen in second Streamlit tab.

**Our Solution:**
- ResizeObserver-based auto-resize detection
- Handles container size changes automatically
- Works correctly when switching between Streamlit tabs
- Optional `auto_resize` parameter (default: True)

**Implementation:**
```typescript
// frontend/src/StCytoscapeComponent.tsx - setupAutoResize()
const resizeObserver = new ResizeObserver(() => {
  cy.resize()
  cy.fit(undefined, 50)
})
resizeObserver.observe(container)
```

### 4. Customizable Highlight Styles (Issue #63)

**Original Issue:** [Issue #63](https://github.com/AlrasheedA/st-link-analysis/issues/63) requested the ability to customize highlight/selection styles.

**Our Solution:**
- New `HighlightStyle` class for full control over selection appearance
- Separate customization for node and edge highlights
- Support for custom_styles in highlights too
- Sensible defaults if not specified

**Implementation:**
```python
# st_cytoscape/styles.py - HighlightStyle class
class HighlightStyle:
    def __init__(
        self,
        node_color=None,
        node_border_width=3,
        node_border_color="#FFD700",
        edge_color=None,
        edge_width=None,
        custom_styles=None
    )
```

## Project Structure

```
st-cytoscape/
├── st_cytoscape/              # Python package
│   ├── __init__.py           # Package exports
│   ├── component.py          # Main Streamlit component
│   ├── styles.py             # Style classes (Node, Edge, Highlight)
│   └── events.py             # Event handling
├── frontend/                  # React/TypeScript frontend
│   ├── src/
│   │   ├── StCytoscapeComponent.tsx  # Main React component
│   │   └── index.tsx         # Entry point
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── examples/                  # Example applications
│   ├── comprehensive_demo.py # Full feature demonstration
│   └── simple_example.py     # Basic usage
├── tests/                     # Unit tests
│   ├── test_styles.py
│   └── test_component.py
├── setup.py                   # Package configuration
├── README.md                  # User documentation
├── CONTRIBUTING.md            # Contributor guide
└── LICENSE                    # MIT License
```

## Key Features

### Python API

1. **Flexible Style System**
   - `NodeStyle` with custom_styles, icons, positioning
   - `EdgeStyle` with custom_styles, directional arrows
   - `HighlightStyle` for selection appearance

2. **Helper Functions**
   - `create_node()` - Easy node creation with positioning
   - `create_edge()` - Easy edge creation

3. **Comprehensive Options**
   - Multiple layout algorithms
   - Event handling (clicks, selection changes)
   - Configurable interactions (pan, zoom, box selection)

### Frontend Implementation

1. **Cytoscape.js Integration**
   - Full Cytoscape.js feature support
   - Dynamic style generation from Python objects
   - Material icon support

2. **Auto-Resize Fix**
   - ResizeObserver for container changes
   - Window resize handling
   - Proper multi-tab support

3. **Type Safety**
   - TypeScript for compile-time checking
   - Proper typing for all components

## Minimal Changes Philosophy

The project addresses the issues with **minimal changes** by:

1. **Reusing proven patterns** from st-link-analysis
2. **Focusing on the core issues** rather than adding unnecessary features
3. **Maintaining simple API** that's easy to understand
4. **Using standard tools** (ResizeObserver, Cytoscape.js built-ins)
5. **Adding flexibility hooks** (custom_styles) rather than exposing every option

## Testing

Unit tests cover:
- Style class creation and serialization
- Helper function behavior
- Custom styles integration
- Coordinate positioning

Run tests:
```bash
pytest tests/
```

## Examples

The `examples/` directory demonstrates:

1. **simple_example.py** - Basic usage in ~20 lines
2. **comprehensive_demo.py** - All features including:
   - Multi-tab support (Issue #35 fix)
   - Custom styling (PR #62)
   - Coordinate positioning (Issue #44)
   - Customizable highlights (Issue #63)

## Development Workflow

1. **Frontend development:**
   ```bash
   cd frontend && npm start
   ```

2. **Test with Streamlit:**
   ```bash
   streamlit run examples/comprehensive_demo.py
   ```

3. **Build for production:**
   ```bash
   cd frontend && npm run build
   ```

## Future Enhancements

Potential additions based on other st-link-analysis issues:

- **Issue #64**: Export graph as image
- **Issue #59**: Enhanced search/zoom/highlight
- **Issue #33**: Edge thickness based on data
- **Issue #51**: Additional layout algorithms (Klay)

These can be added incrementally while maintaining the core flexibility.

## Comparison with st-link-analysis

| Feature | st-link-analysis | st-cytoscape |
|---------|------------------|--------------|
| Custom Cytoscape.js styles | ❌ (PR pending) | ✅ Built-in |
| Coordinate positioning | ❌ | ✅ |
| Multi-tab auto-resize | ❌ (Bug) | ✅ Fixed |
| Custom highlight styles | ❌ | ✅ |
| Material icons | ✅ | ✅ |
| Layout algorithms | ✅ | ✅ |
| Interactive events | ✅ | ✅ |
| Active maintenance | ❓ | ✅ |

## Conclusion

st-cytoscape successfully addresses the key customization and flexibility issues in st-link-analysis with minimal changes to the core architecture. The focus on built-in extensibility (custom_styles) and proper component lifecycle handling (auto-resize) provides a solid foundation for future enhancements.
