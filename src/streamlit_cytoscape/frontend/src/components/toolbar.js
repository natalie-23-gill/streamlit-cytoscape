import State from "../utils/state";
import { debounce, getCyInstance } from "../utils/helpers";

// Constants / Configurations
const IDS = {
    fullscreen: "toolbarFullscreen",
    refresh: "toolbarRefresh",
    export: "toolbarExport",
};
const DELAYS = {
    default: 150,
    fullscreen: 100,
    refresh: 200,
};

// Event Handlers
const clickHandlers = {
    fullscreen: debounce(() => {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            document.getElementById("container").requestFullscreen();
        }
    }, DELAYS.fullscreen),

    refresh: debounce(() => {
        const cy = getCyInstance();
        cy.layout(State.getState("layout")).run();
    }, DELAYS.refresh),

    export: () => {
        const dialog = document.getElementById("exportDialog");
        const filenameInput = document.getElementById("exportFilename");
        filenameInput.value = "graph";
        document.getElementById("exportIncludeStyles").checked = false;
        dialog.showModal();
        filenameInput.select();
    },
};

function performExport() {
    const cy = getCyInstance();
    const filenameInput = document.getElementById("exportFilename");
    const includeStyles = document.getElementById("exportIncludeStyles").checked;
    const dialog = document.getElementById("exportDialog");

    const fullJson = cy.json();
    const visibleIds = new Set(
        cy
            .elements()
            .not(":hidden")
            .map((ele) => ele.id())
    );

    const nodes = (fullJson.elements.nodes || []).filter((n) =>
        visibleIds.has(n.data.id)
    );
    const edges = (fullJson.elements.edges || []).filter((e) =>
        visibleIds.has(e.data.id)
    );

    const exportData = { elements: { nodes, edges } };

    if (includeStyles) {
        exportData.style = cy.style().json();
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const filename = (filenameInput.value.trim() || "graph") + ".json";
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    dialog.close();
}

// Toolbar initialization
function initToolbar() {
    document
        .getElementById(IDS.fullscreen)
        .addEventListener("click", clickHandlers.fullscreen);
    document
        .getElementById(IDS.refresh)
        .addEventListener("click", clickHandlers.refresh);
    document
        .getElementById(IDS.export)
        .addEventListener("click", clickHandlers.export);

    document
        .getElementById("exportConfirm")
        .addEventListener("click", performExport);
    document
        .getElementById("exportCancel")
        .addEventListener("click", () =>
            document.getElementById("exportDialog").close()
        );
}

export default initToolbar;
