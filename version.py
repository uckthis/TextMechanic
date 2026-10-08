"""
Text Mechanic — version metadata.

This is the single source of truth for the app's version. Bump
__version__ here and rebuild; both the running app and the PyInstaller
exe pick it up automatically.

Format: MAJOR.MINOR.PATCH (semver-ish)
  - MAJOR: breaking UI changes or removed features
  - MINOR: new tools, new themes, new layouts
  - PATCH: bug fixes, small polish, no behavior change
"""

__version__ = "1.1.2"
__app_name__ = "Text Mechanic"
__app_description__ = "A modern toolbox for transforming, cleaning, and analyzing text."
__app_author__ = "Waqas"
__app_org__ = "Antigravity"
__app_domain__ = "antigravity.local"
__build_date__ = "2026-10-08"


def full_version_string() -> str:
    """Long-form version with build date — for About dialog / status bar."""
    return f"{__app_name__} v{__version__} (built {__build_date__})"


def short_version_string() -> str:
    """Short version for compact UI elements (status bar)."""
    return f"{__app_name__} v{__version__}"
