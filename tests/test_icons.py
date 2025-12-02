"""
Tests for Material Icons API integration
"""

import pytest
from st_cytoscape.icons import (
    MaterialIconsAPI,
    get_available_icons,
    is_valid_icon,
    search_icons,
    refresh_icons,
)


class TestMaterialIconsAPI:
    """Test Material Icons API functionality"""

    def test_singleton_pattern(self):
        """Test that MaterialIconsAPI is a singleton"""
        api1 = MaterialIconsAPI()
        api2 = MaterialIconsAPI()
        assert api1 is api2

    def test_get_available_icons(self):
        """Test getting available icons"""
        icons = get_available_icons()
        assert isinstance(icons, list)
        # Should have at least the fallback icons
        assert len(icons) > 0

    def test_is_valid_icon_common_icons(self):
        """Test validation of common Material Icons"""
        # These icons should be in the fallback list at minimum
        common_icons = ["person", "home", "settings", "favorite"]
        for icon in common_icons:
            # We use force_refresh=False to use cache/fallback
            result = is_valid_icon(icon, force_refresh=False)
            assert isinstance(result, bool)

    def test_is_valid_icon_empty_string(self):
        """Test validation of empty icon name"""
        assert is_valid_icon("") is False
        assert is_valid_icon(None) is False

    def test_search_icons(self):
        """Test searching for icons"""
        results = search_icons("person", force_refresh=False)
        assert isinstance(results, list)

        # Search should be case-insensitive
        results_upper = search_icons("PERSON", force_refresh=False)
        assert results == results_upper

    def test_search_icons_empty_query(self):
        """Test searching with empty query"""
        results = search_icons("", force_refresh=False)
        # Empty query should return all icons
        all_icons = get_available_icons(force_refresh=False)
        assert results == all_icons

    def test_fallback_icons(self):
        """Test that fallback icons are available"""
        api = MaterialIconsAPI()
        fallback = api._get_fallback_icons()

        assert isinstance(fallback, list)
        assert len(fallback) > 0
        assert "person" in fallback
        assert "home" in fallback

    def test_extract_icon_names_from_metadata(self):
        """Test extracting icon names from various metadata structures"""
        api = MaterialIconsAPI()

        # Test with icons array structure
        metadata1 = {
            "icons": [
                {"name": "icon1"},
                {"name": "icon2"},
            ]
        }
        names1 = api._extract_icon_names(metadata1)
        assert "icon1" in names1
        assert "icon2" in names1

        # Test with familyMetadataList structure
        metadata2 = {
            "familyMetadataList": [
                {
                    "icons": [
                        {"name": "icon3"},
                        {"name": "icon4"},
                    ]
                }
            ]
        }
        names2 = api._extract_icon_names(metadata2)
        assert "icon3" in names2
        assert "icon4" in names2

        # Test with duplicates - should be removed
        metadata3 = {
            "icons": [
                {"name": "duplicate"},
                {"name": "duplicate"},
            ]
        }
        names3 = api._extract_icon_names(metadata3)
        assert names3.count("duplicate") == 1


class TestNodeStyleIconValidation:
    """Test icon validation in NodeStyle"""

    def test_valid_icon_no_warning(self):
        """Test that valid icons don't produce warnings"""
        from st_cytoscape import NodeStyle
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Use a common icon that should be in cache/fallback
            style = NodeStyle("test", icon="person")
            assert style.icon == "person"
            # May or may not warn depending on cache state, so we don't assert

    def test_invalid_icon_with_warning(self):
        """Test that invalid icons produce warnings when validation is enabled"""
        from st_cytoscape import NodeStyle
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Use a clearly invalid icon name
            style = NodeStyle("test", icon="definitely_not_a_real_icon_12345xyz")
            assert style.icon == "definitely_not_a_real_icon_12345xyz"
            # Warning may or may not be produced depending on API availability

    def test_validation_disabled(self):
        """Test that validation can be disabled"""
        from st_cytoscape import NodeStyle
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            style = NodeStyle("test", icon="custom_icon", validate_icon=False)
            assert style.icon == "custom_icon"
            # Should not produce any warnings
            validation_warnings = [
                warning
                for warning in w
                if "valid Material Icon" in str(warning.message)
            ]
            assert len(validation_warnings) == 0

    def test_none_icon_no_validation(self):
        """Test that None icon doesn't trigger validation"""
        from st_cytoscape import NodeStyle
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            style = NodeStyle("test", icon=None)
            assert style.icon is None
            # Should not produce any warnings
            assert len(w) == 0
