from typing import Optional, Dict, Any

from streamlit_cytoscape.events import RESERVED_NAMES


class InfopanelAction:
    def __init__(
        self,
        name: str,
        label: str,
        icon: Optional[str] = None,
    ) -> None:
        """
        Define a custom action button for the infopanel.

        Parameters
        ----------
        name : str
            Unique action name returned in the component value
            when the button is clicked. Must not be a reserved name
            (remove, expand, expand_edge).
        label : str
            Display text for the button.
        icon : Optional[str]
            Icon for the button. Can be a Material Icons name
            (e.g., "search") or a url(...) string. A list of
            supported icons is available in `streamlit_cytoscape.icons`.
        """
        if name in RESERVED_NAMES:
            raise ValueError(f"{RESERVED_NAMES} are reserved action names")
        self.name = name
        self.label = label
        self.icon = icon

    def dump(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "label": self.label,
        }
        if self.icon is not None:
            result["icon"] = self.icon
        return result
