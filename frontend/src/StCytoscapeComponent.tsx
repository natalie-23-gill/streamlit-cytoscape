import React, { useEffect, useRef, useState } from "react"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import cytoscape, { Core, EventObject, NodeSingular, EdgeSingular } from "cytoscape"

interface StCytoscapeProps {
  args: {
    elements: any[]
    node_styles: any[]
    edge_styles: any[]
    layout: string
    height: number | string
    width: number | string
    selection_type: string
    highlight_style: any
    enable_physics: boolean
    pan_enabled: boolean
    zoom_enabled: boolean
    boxselection_enabled: boolean
    auto_resize: boolean
  }
}

/**
 * Main Cytoscape component with enhanced flexibility
 *
 * Addresses:
 * - Issue #35: Auto-resize support for multi-tab scenarios
 * - Issue #63: Customizable highlight styles
 * - PR #62: Custom styles support
 */
const StCytoscapeComponent: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null)
  const cyRef = useRef<Core | null>(null)
  const resizeObserverRef = useRef<ResizeObserver | null>(null)
  const [props, setProps] = useState<StCytoscapeProps["args"] | null>(null)

  useEffect(() => {
    // Receive props from Streamlit
    const onRender = (event: Event) => {
      const data = (event as CustomEvent).detail
      setProps(data.args)
      Streamlit.setFrameHeight()
    }

    window.addEventListener("message", onRender)
    return () => window.removeEventListener("message", onRender)
  }, [])

  useEffect(() => {
    if (!containerRef.current || !props) return

    // Initialize Cytoscape
    const cy = cytoscape({
      container: containerRef.current,
      elements: props.elements || [],
      style: buildCytoscapeStyles(props.node_styles, props.edge_styles, props.highlight_style),
      layout: { name: props.layout || "cose" },
      userPanningEnabled: props.pan_enabled !== false,
      userZoomingEnabled: props.zoom_enabled !== false,
      boxSelectionEnabled: props.boxselection_enabled || false,
      selectionType: props.selection_type || "single",
      autoungrabify: false,
      autounselectify: false,
    })

    cyRef.current = cy

    // Fix for Issue #35: Auto-resize support
    if (props.auto_resize !== false) {
      setupAutoResize(cy, containerRef.current)
    }

    // Event handlers
    setupEventHandlers(cy)

    // Initial fit
    cy.fit(undefined, 50)

    return () => {
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect()
      }
      cy.destroy()
    }
  }, [props])

  const setupAutoResize = (cy: Core, container: HTMLElement) => {
    // Fix for Issue #35: Use ResizeObserver to handle container size changes
    // This fixes the multi-tab rendering issue
    const resizeObserver = new ResizeObserver(() => {
      cy.resize()
      cy.fit(undefined, 50)
    })

    resizeObserver.observe(container)
    resizeObserverRef.current = resizeObserver

    // Also handle window resize
    const handleResize = () => {
      cy.resize()
      cy.fit(undefined, 50)
    }
    window.addEventListener("resize", handleResize)

    return () => {
      resizeObserver.disconnect()
      window.removeEventListener("resize", handleResize)
    }
  }

  const setupEventHandlers = (cy: Core) => {
    // Node click
    cy.on("tap", "node", (evt: EventObject) => {
      const node = evt.target as NodeSingular
      sendEvent({
        type: "node_click",
        target: node.data(),
        selected_nodes: cy.nodes(":selected").map(n => n.id()),
        selected_edges: cy.edges(":selected").map(e => e.id()),
      })
    })

    // Edge click
    cy.on("tap", "edge", (evt: EventObject) => {
      const edge = evt.target as EdgeSingular
      sendEvent({
        type: "edge_click",
        target: edge.data(),
        selected_nodes: cy.nodes(":selected").map(n => n.id()),
        selected_edges: cy.edges(":selected").map(e => e.id()),
      })
    })

    // Background click
    cy.on("tap", (evt: EventObject) => {
      if (evt.target === cy) {
        sendEvent({
          type: "background_click",
          selected_nodes: cy.nodes(":selected").map(n => n.id()),
          selected_edges: cy.edges(":selected").map(e => e.id()),
        })
      }
    })

    // Selection change
    cy.on("select unselect", () => {
      sendEvent({
        type: "selection_change",
        selected_nodes: cy.nodes(":selected").map(n => n.id()),
        selected_edges: cy.edges(":selected").map(e => e.id()),
      })
    })
  }

  const sendEvent = (eventData: any) => {
    Streamlit.setComponentValue(eventData)
  }

  const heightStyle = typeof props?.height === "number" ? `${props.height}px` : props?.height || "600px"
  const widthStyle = typeof props?.width === "number" ? `${props.width}px` : props?.width || "100%"

  return (
    <div
      ref={containerRef}
      style={{
        width: widthStyle,
        height: heightStyle,
        border: "1px solid #ddd",
        borderRadius: "4px",
      }}
    />
  )
}

/**
 * Build Cytoscape.js styles from Python style objects
 * Supports custom_styles for maximum flexibility (PR #62)
 */
function buildCytoscapeStyles(
  nodeStyles: any[],
  edgeStyles: any[],
  highlightStyle: any
): any[] {
  const styles: any[] = []

  // Node styles
  if (nodeStyles) {
    nodeStyles.forEach((style) => {
      const baseStyle: any = {
        selector: `node[type = "${style.type}"]`,
        style: {
          "background-color": style.color,
          width: style.size,
          height: style.size,
          label: style.caption ? `data(${style.caption})` : "",
          "text-valign": "center",
          "text-halign": "center",
          "font-size": "12px",
          ...style.custom_styles, // PR #62: Apply custom styles
        },
      }

      // Add icon support
      if (style.icon) {
        baseStyle.style["background-image"] = "none"
        baseStyle.style["text-valign"] = "center"
        baseStyle.style["text-halign"] = "center"
        baseStyle.style["font-family"] = "Material Icons"
        baseStyle.style["label"] = style.icon
        baseStyle.style["font-size"] = `${Math.max(style.size * 0.6, 16)}px`
        baseStyle.style["color"] = "#fff"
      }

      styles.push(baseStyle)
    })
  }

  // Edge styles
  if (edgeStyles) {
    edgeStyles.forEach((style) => {
      const baseStyle: any = {
        selector: `edge[type = "${style.type}"]`,
        style: {
          "line-color": style.color,
          width: style.width,
          label: style.caption ? `data(${style.caption})` : "",
          "font-size": "10px",
          "text-rotation": "autorotate",
          "text-margin-y": -10,
          ...style.custom_styles, // PR #62: Apply custom styles
        },
      }

      if (style.directed) {
        baseStyle.style["target-arrow-color"] = style.color
        baseStyle.style["target-arrow-shape"] = "triangle"
        baseStyle.style["curve-style"] = "bezier"
      }

      styles.push(baseStyle)
    })
  }

  // Default node style
  styles.push({
    selector: "node",
    style: {
      "background-color": "#666",
      width: 40,
      height: 40,
      label: "data(label)",
    },
  })

  // Default edge style
  styles.push({
    selector: "edge",
    style: {
      "line-color": "#ccc",
      width: 2,
    },
  })

  // Issue #63: Customizable highlight styles
  if (highlightStyle) {
    styles.push({
      selector: "node:selected",
      style: {
        "background-color": highlightStyle.node_color || undefined,
        "border-width": highlightStyle.node_border_width,
        "border-color": highlightStyle.node_border_color,
        ...highlightStyle.custom_styles,
      },
    })

    styles.push({
      selector: "edge:selected",
      style: {
        "line-color": highlightStyle.edge_color || undefined,
        width: highlightStyle.edge_width || undefined,
        ...highlightStyle.custom_styles,
      },
    })
  } else {
    // Default highlight styles
    styles.push({
      selector: "node:selected",
      style: {
        "border-width": 3,
        "border-color": "#FFD700",
      },
    })

    styles.push({
      selector: "edge:selected",
      style: {
        "line-color": "#FFD700",
      },
    })
  }

  return styles
}

export default withStreamlitConnection(StCytoscapeComponent)
