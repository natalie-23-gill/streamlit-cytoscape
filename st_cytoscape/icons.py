"""
Material Icons API integration for st-cytoscape

Fetches and caches Material Icons metadata from Google Fonts API
"""

import json
import os
from typing import List, Optional, Dict, Any
from pathlib import Path
import urllib.request
import urllib.error


class MaterialIconsAPI:
    """
    Utility class for fetching and validating Material Icons from Google Fonts API
    """

    METADATA_URL = "https://fonts.google.com/metadata/icons"
    CACHE_FILE = Path(__file__).parent / ".material_icons_cache.json"

    _instance = None
    _icons_cache: Optional[List[str]] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MaterialIconsAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the Material Icons API client"""
        if self._icons_cache is None:
            self._load_cache()

    def _fetch_metadata(self) -> Dict[str, Any]:
        """
        Fetch icon metadata from Google Fonts API

        Returns:
            Dictionary containing icon metadata

        Raises:
            urllib.error.URLError: If the request fails
        """
        try:
            with urllib.request.urlopen(self.METADATA_URL) as response:
                data = response.read().decode("utf-8")

                # Remove the XSSI protection prefix )]}' from the response
                if data.startswith(")]}'\n"):
                    data = data[5:]
                elif data.startswith(")]}'"):
                    data = data[4:]

                return json.loads(data)
        except urllib.error.URLError as e:
            raise Exception(f"Failed to fetch Material Icons metadata: {e}")

    def _extract_icon_names(self, metadata: Dict[str, Any]) -> List[str]:
        """
        Extract icon names from metadata

        Args:
            metadata: Raw metadata from Google Fonts API

        Returns:
            List of icon names
        """
        icon_names = []

        # The metadata structure has icons in familyMetadataList or icons array
        if "icons" in metadata:
            for icon in metadata.get("icons", []):
                if "name" in icon:
                    icon_names.append(icon["name"])

        # Also check for familyMetadataList structure
        if "familyMetadataList" in metadata:
            for family in metadata.get("familyMetadataList", []):
                if "icons" in family:
                    for icon in family["icons"]:
                        if "name" in icon:
                            icon_names.append(icon["name"])

        return sorted(list(set(icon_names)))  # Remove duplicates and sort

    def _save_cache(self, icon_names: List[str]) -> None:
        """
        Save icon names to local cache file

        Args:
            icon_names: List of icon names to cache
        """
        try:
            cache_data = {"version": "1.0", "icons": icon_names}
            with open(self.CACHE_FILE, "w") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            # Cache write failure is not critical
            print(f"Warning: Failed to save icon cache: {e}")

    def _load_cache(self) -> None:
        """
        Load icon names from local cache file
        Sets _icons_cache to the cached list if available
        """
        if self.CACHE_FILE.exists():
            try:
                with open(self.CACHE_FILE, "r") as f:
                    cache_data = json.load(f)
                    self._icons_cache = cache_data.get("icons", [])
            except Exception as e:
                print(f"Warning: Failed to load icon cache: {e}")
                self._icons_cache = None

    def refresh_icons(self) -> List[str]:
        """
        Fetch fresh icon list from Google Fonts API and update cache

        Returns:
            List of available icon names

        Raises:
            Exception: If fetching metadata fails
        """
        metadata = self._fetch_metadata()
        icon_names = self._extract_icon_names(metadata)

        if icon_names:
            self._icons_cache = icon_names
            self._save_cache(icon_names)

        return icon_names

    def get_available_icons(self, force_refresh: bool = False) -> List[str]:
        """
        Get list of available Material Icons

        Args:
            force_refresh: If True, fetch fresh data from API instead of using cache

        Returns:
            List of available icon names
        """
        if force_refresh or self._icons_cache is None:
            try:
                return self.refresh_icons()
            except Exception as e:
                # If refresh fails and we have cache, use it
                if self._icons_cache is not None:
                    print(f"Warning: Using cached icons due to API error: {e}")
                    return self._icons_cache
                else:
                    # No cache available, return common icons as fallback
                    print(f"Warning: Using fallback icon list due to API error: {e}")
                    return self._get_fallback_icons()

        return self._icons_cache or []

    def _get_fallback_icons(self) -> List[str]:
        """
        Get a fallback list of common Material Icons when API is unavailable

        Returns:
            List of common icon names
        """
        return [
            "person",
            "folder",
            "hub",
            "location_on",
            "home",
            "settings",
            "favorite",
            "search",
            "info",
            "help",
            "check_circle",
            "star",
            "delete",
            "add",
            "remove",
            "edit",
            "save",
            "cloud",
            "download",
            "upload",
            "attach_file",
            "email",
            "phone",
            "work",
            "school",
            "shopping_cart",
            "calendar_today",
            "schedule",
            "lock",
            "visibility",
            "notifications",
            "account_circle",
            "dashboard",
            "explore",
            "language",
        ]

    def is_valid_icon(self, icon_name: str, force_refresh: bool = False) -> bool:
        """
        Check if an icon name is valid

        Args:
            icon_name: Name of the icon to validate
            force_refresh: If True, fetch fresh data from API

        Returns:
            True if icon name is valid, False otherwise
        """
        if not icon_name:
            return False

        available_icons = self.get_available_icons(force_refresh=force_refresh)
        return icon_name in available_icons

    def search_icons(self, query: str, force_refresh: bool = False) -> List[str]:
        """
        Search for icons matching a query string

        Args:
            query: Search query (case-insensitive)
            force_refresh: If True, fetch fresh data from API

        Returns:
            List of matching icon names
        """
        available_icons = self.get_available_icons(force_refresh=force_refresh)
        query_lower = query.lower()

        return [icon for icon in available_icons if query_lower in icon.lower()]


# Singleton instance
_icons_api = MaterialIconsAPI()


def get_available_icons(force_refresh: bool = False) -> List[str]:
    """
    Get list of available Material Icons

    Args:
        force_refresh: If True, fetch fresh data from API instead of using cache

    Returns:
        List of available icon names
    """
    return _icons_api.get_available_icons(force_refresh=force_refresh)


def is_valid_icon(icon_name: str, force_refresh: bool = False) -> bool:
    """
    Check if an icon name is valid

    Args:
        icon_name: Name of the icon to validate
        force_refresh: If True, fetch fresh data from API

    Returns:
        True if icon name is valid, False otherwise
    """
    return _icons_api.is_valid_icon(icon_name, force_refresh=force_refresh)


def search_icons(query: str, force_refresh: bool = False) -> List[str]:
    """
    Search for icons matching a query string

    Args:
        query: Search query (case-insensitive)
        force_refresh: If True, fetch fresh data from API

    Returns:
        List of matching icon names
    """
    return _icons_api.search_icons(query, force_refresh=force_refresh)


def refresh_icons() -> List[str]:
    """
    Refresh the icon list from Google Fonts API

    Returns:
        List of available icon names
    """
    return _icons_api.refresh_icons()
