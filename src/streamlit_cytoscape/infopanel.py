from typing import Optional, Dict, Any

from streamlit_cytoscape.events import RESERVED_NAMES


class InfopanelAction:
    def __init__(
        self,
        name: str,
        label: str,
        icon: Optional[str] = None,
        spinner: bool = False,
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
        spinner : bool, default False
            If True, the button shows an instant busy spinner the
            moment it is clicked (cleared on the next render). Use
            this for long-running or asynchronous actions (e.g. an
            action that kicks off a background API call) so the user
            gets immediate feedback while the work is in flight.
        """
        if name in RESERVED_NAMES:
            raise ValueError(f"{RESERVED_NAMES} are reserved action names")
        self.name = name
        self.label = label
        self.icon = icon
        self.spinner = spinner

    def dump(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "label": self.label,
        }
        if self.icon is not None:
            result["icon"] = self.icon
        if self.spinner:
            result["spinner"] = True
        return result
