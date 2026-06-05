import State from "../utils/state";
import { debouncedSetValue } from "../utils/helpers";

// Constants / Configurations
const INFOPANEL_ID = "infopanel";
const LABEL_ID = "infopanelLabel";
const PROPS_ID = "infopanelProps";
const NODEACTIONS_ID = "nodeActions";
const ACTIONS_ID = "infopanelActions";
const RESIZE_ID = "infopanelResize";

// Module-level configuration
let hideUnderscoreAttrs = true;

// Persisted panel width (default matches original CSS)
let panelWidth = "17.5rem";

function initInfopanel(hideUnderscore) {
    hideUnderscoreAttrs = hideUnderscore;
}

// Infopanel children updates
function _updateLabel(color, label, icon) {
    const label_div = document.getElementById(LABEL_ID);
    label_div.firstChild.innerText = label;
    label_div.firstChild.style.borderColor = color;
    label_div.lastChild.style.backgroundColor = color;
    if (icon && icon != "none") {
        label_div.lastChild.style.backgroundImage = `url(${icon})`;
    } else {
        label_div.lastChild.style.backgroundImage = "";
    }
}

// Only http(s) links are allowed; everything else renders as inert text.
const ALLOWED_SCHEME = /^https?:\/\//i;
// Matches <a ... href="URL" ...>TEXT</a> with single- or double-quoted href.
const ANCHOR_RE =
    /<a\b[^>]*\bhref\s*=\s*("([^"]*)"|'([^']*)')[^>]*>([\s\S]*?)<\/a>/gi;

// Safely render a value that may contain <a href> links. We never use
// innerHTML: surrounding text becomes text nodes and each anchor is rebuilt
// via the DOM API, copying only a scheme-checked href (no onclick/onerror,
// no other tags), so no arbitrary HTML/script can execute.
function _appendLinkified(parent, value) {
    const text = String(value);
    let lastIndex = 0;
    let m;
    ANCHOR_RE.lastIndex = 0;
    while ((m = ANCHOR_RE.exec(text)) !== null) {
        if (m.index > lastIndex) {
            parent.appendChild(
                document.createTextNode(text.slice(lastIndex, m.index))
            );
        }
        const href = m[2] !== undefined ? m[2] : m[3];
        const linkText = m[4].replace(/<[^>]*>/g, ""); // strip nested tags
        if (ALLOWED_SCHEME.test(href)) {
            const a = document.createElement("a");
            a.href = href;
            a.target = "_blank";
            a.rel = "noopener noreferrer";
            a.textContent = linkText;
            parent.appendChild(a);
        } else {
            // Disallowed scheme (javascript:, data:, ...): show text, no link.
            parent.appendChild(document.createTextNode(linkText));
        }
        lastIndex = ANCHOR_RE.lastIndex;
    }
    if (lastIndex < text.length) {
        parent.appendChild(document.createTextNode(text.slice(lastIndex)));
    }
}

function _updateProps(data) {
    const props = document.getElementById(PROPS_ID);
    props.innerHTML = "";
    Object.entries(data)
        .filter(([key]) => {
            if (key === "label") return false;
            if (hideUnderscoreAttrs && key.startsWith("_")) return false;
            return true;
        })
        .forEach(([key, value]) => {
            const div = document.createElement("div");
            div.className = "infopanel__prop";
            const keyP = document.createElement("p");
            keyP.className = "infopanel__key";
            keyP.textContent = key;
            const valP = document.createElement("p");
            valP.className = "infopanel__val";
            _appendLinkified(valP, value);
            div.appendChild(keyP);
            div.appendChild(valP);
            props.appendChild(div);
        });
}

function initResize() {
    const handle = document.getElementById(RESIZE_ID);
    const infopanel = document.getElementById(INFOPANEL_ID);
    const nodeActions = document.getElementById(NODEACTIONS_ID);
    const container = document.getElementById("container");
    let dragging = false;

    handle.addEventListener("mousedown", (e) => {
        e.preventDefault();
        dragging = true;
        infopanel.classList.add("dragging");
        nodeActions.classList.add("dragging");
    });

    document.addEventListener("mousemove", (e) => {
        if (!dragging) return;
        const containerRect = container.getBoundingClientRect();
        const maxWidth = containerRect.width * 0.5;
        const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
        const minWidth = 12 * rootFontSize;
        let newWidth = e.clientX - containerRect.left - parseFloat(getComputedStyle(infopanel).marginLeft);
        newWidth = Math.max(minWidth, Math.min(newWidth, maxWidth));
        panelWidth = newWidth + "px";
        infopanel.style.width = panelWidth;
        nodeActions.style.left = (newWidth + parseFloat(getComputedStyle(nodeActions).marginLeft) + parseFloat(getComputedStyle(infopanel).marginLeft)) + "px";
    });

    document.addEventListener("mouseup", () => {
        if (!dragging) return;
        dragging = false;
        infopanel.classList.remove("dragging");
        nodeActions.classList.remove("dragging");
    });
}

function initInfopanelActions(actions) {
    if (!actions || actions.length === 0) return;
    const actionsContainer = document.getElementById(ACTIONS_ID);

    actions.forEach((action) => {
        const btn = document.createElement("button");
        btn.className = "infopanel__action-btn";
        btn.setAttribute("data-action-name", action.name);

        if (action.icon) {
            const iconEl = document.createElement("span");
            iconEl.className = "infopanel__action-icon";
            if (action.icon.startsWith("url(")) {
                iconEl.style.backgroundImage = action.icon;
            } else {
                iconEl.style.backgroundImage = `url(./icons/${action.icon.toLowerCase()}.svg)`;
            }
            btn.appendChild(iconEl);
        }

        const labelEl = document.createElement("span");
        labelEl.textContent = action.label;
        btn.appendChild(labelEl);

        btn.addEventListener("click", () => {
            const { selected: eles } = State.getState("selection");
            if (!eles || eles.length === 0) return;
            const ele = eles.first();
            // Instant feedback for long-running/async actions; cleared on the
            // next render (see clearInfopanelBusy in onRender).
            if (action.spinner) {
                btn.classList.add("infopanel__action-btn--busy");
            }
            debouncedSetValue({
                action: action.name,
                data: {
                    element_id: ele.id(),
                    element_group: ele.group(),
                    element_data: ele.data(),
                },
                timestamp: Date.now(),
            });
        });

        actionsContainer.appendChild(btn);
    });
}

// Clear any in-flight busy spinners on action buttons. Called at the start of
// each render so the spinner lasts from click until the rerun completes.
function clearInfopanelBusy() {
    document
        .querySelectorAll(".infopanel__action-btn--busy")
        .forEach((b) => b.classList.remove("infopanel__action-btn--busy"));
}

// infopanel update
function updateInfopanel() {
    const infopanel = document.getElementById(INFOPANEL_ID);
    const nodeActions = document.getElementById(NODEACTIONS_ID);
    const { selected: eles } = State.getState("selection");
    let color, data, label, expanded, icon;
    if (eles?.length === 1) {
        color = eles.first().style().backgroundColor;
        data = eles.first().data();
        label = data["label"] || eles.group().slice(0, -1).toUpperCase();
        expanded = true;
        icon = eles.style()["background-image"];
    } else {
        color = "hsla(0, 0%, 0%, 0)";
        data = {};
        label = "";
        expanded = false;
        icon = null;
    }
    infopanel.setAttribute("data-expanded", expanded);
    nodeActions.setAttribute("data-expanded", expanded);

    if (expanded) {
        infopanel.style.width = panelWidth;
        const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
        const marginLeft = parseFloat(getComputedStyle(infopanel).marginLeft);
        const nodeActionsMargin = parseFloat(getComputedStyle(nodeActions).marginLeft);
        const widthPx = infopanel.getBoundingClientRect().width;
        nodeActions.style.left = (widthPx + nodeActionsMargin + marginLeft) + "px";
    } else {
        infopanel.style.width = "";
        nodeActions.style.left = "";
    }

    _updateLabel(color, label, icon);
    _updateProps(data);
}

export {
    initInfopanel,
    initResize,
    initInfopanelActions,
    clearInfopanelBusy,
};
export default updateInfopanel;
