"""
Theme Manager for Text Mechanic.
Five carefully crafted themes with a modern minimal design language.

Themes:
  - Daylight (light, amber)    — primary light, warm gold
  - Dark     (dark, amber)     — primary dark, the "opposite of Daylight"
  - Sunset   (light, orange)   — vibrant warm orange
  - Blush    (light, pink)     — soft romantic pink
  - Forest   (dark, emerald)   — nature-inspired dark green

Older versions of the app used "Snow" as the name for the dark amber
theme. THEME_ALIASES handles the migration transparently.
"""

# Theme migration: old name -> new name
THEME_ALIASES: dict[str, str] = {
    "Slate":   "Dark",
    "Snow":    "Dark",
    "Midnight": "Dark",
}

# ──────────────────────────────────────────────────────────────────────
#  PALETTES
# ──────────────────────────────────────────────────────────────────────
PALETTES = {
    # ── Daylight: warm off-white with amber/gold accent ────────────
    "Daylight": {
        "bg":               "#FAFAF9",
        "surface":          "#FFFFFF",
        "surface_2":        "#F5F5F4",
        "border":           "#E7E5E4",
        "border_strong":    "#D6D3D1",
        "text":             "#1C1917",
        "text_dim":         "#57534E",
        "text_faint":       "#A8A29E",
        "accent":           "#D97706",
        "accent_soft":      "#F59E0B",
        "accent_fg":        "#FFFFFF",
        "accent_soft_bg":   "#FEF3C7",
        "accent_soft_fg":   "#92400E",
        "success":          "#059669",
        "danger":           "#DC2626",
        "shadow":           "rgba(28, 25, 23, 0.06)",
        "shadow_strong":    "rgba(28, 25, 23, 0.12)",
    },
    # ── Dark: deep neutral dark with amber accent ──────────────────
    "Dark": {
        "bg":               "#0C0A09",
        "surface":          "#1C1917",
        "surface_2":        "#292524",
        "border":           "#292524",
        "border_strong":    "#44403C",
        "text":             "#FAFAF9",
        "text_dim":         "#A8A29E",
        "text_faint":       "#57534E",
        "accent":           "#F59E0B",
        "accent_soft":      "#FBBF24",
        "accent_fg":        "#1C1917",
        "accent_soft_bg":   "#422006",
        "accent_soft_fg":   "#FCD34D",
        "success":          "#10B981",
        "danger":           "#F87171",
        "shadow":           "rgba(0, 0, 0, 0.35)",
        "shadow_strong":    "rgba(0, 0, 0, 0.55)",
    },
    # ── Sunset: light warm with deeper, more visible orange accent ──
    "Sunset": {
        "bg":               "#FFEDD5",
        "surface":          "#FFF7ED",
        "surface_2":        "#FED7AA",
        "border":           "#FDBA74",
        "border_strong":    "#FB923C",
        "text":             "#431407",
        "text_dim":         "#7C2D12",
        "text_faint":       "#9A3412",
        "accent":           "#C2410C",
        "accent_soft":      "#EA580C",
        "accent_fg":        "#FFFFFF",
        "accent_soft_bg":   "#FED7AA",
        "accent_soft_fg":   "#7C2D12",
        "success":          "#15803D",
        "danger":           "#B91C1C",
        "shadow":           "rgba(124, 45, 18, 0.08)",
        "shadow_strong":    "rgba(124, 45, 18, 0.16)",
    },
    # ── Blush: light with soft pink accent ───────────────────────
    "Blush": {
        "bg":               "#FDF2F8",
        "surface":          "#FFFFFF",
        "surface_2":        "#FCE7F3",
        "border":           "#FBCFE8",
        "border_strong":    "#F9A8D4",
        "text":             "#500724",
        "text_dim":         "#831843",
        "text_faint":       "#BE185D",
        "accent":           "#DB2777",
        "accent_soft":      "#EC4899",
        "accent_fg":        "#FFFFFF",
        "accent_soft_bg":   "#FCE7F3",
        "accent_soft_fg":   "#9D174D",
        "success":          "#059669",
        "danger":           "#BE123C",
        "shadow":           "rgba(157, 23, 77, 0.06)",
        "shadow_strong":    "rgba(157, 23, 77, 0.12)",
    },
    # ── Forest: dark with emerald accent ─────────────────────────
    "Forest": {
        "bg":               "#052E20",
        "surface":          "#0A3A2A",
        "surface_2":        "#0F4A37",
        "border":           "#0F4A37",
        "border_strong":    "#16694F",
        "text":             "#ECFDF5",
        "text_dim":         "#A7F3D0",
        "text_faint":       "#6EE7B7",
        "accent":           "#10B981",
        "accent_soft":      "#34D399",
        "accent_fg":        "#052E20",
        "accent_soft_bg":   "#064E3B",
        "accent_soft_fg":   "#A7F3D0",
        "success":          "#34D399",
        "danger":           "#FCA5A5",
        "shadow":           "rgba(0, 0, 0, 0.45)",
        "shadow_strong":    "rgba(0, 0, 0, 0.65)",
    },
}


# ──────────────────────────────────────────────────────────────────────
#  QSS TEMPLATE
# ──────────────────────────────────────────────────────────────────────
QSS_TEMPLATE = """
/* ═══════════════════════════════════════════════════════════
   GLOBAL
   ═══════════════════════════════════════════════════════════ */
* {{
    font-family: "Inter", "Segoe UI", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    font-size: 13px;
    color: {text};
    outline: 0;
}}

QMainWindow {{
    background-color: {bg};
}}

QWidget {{
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════════
   TOP BAR
   ═══════════════════════════════════════════════════════════ */
#topBar {{
    background-color: {surface};
    border-bottom: 1px solid {border};
}}

#brandMark {{
    background-color: {accent};
    color: {accent_fg};
    border-radius: 8px;
    font-weight: 800;
    font-size: 14px;
    qproperty-alignment: AlignCenter;
}}

#brandText {{
    color: {text};
    font-weight: 700;
    font-size: 14px;
    background: transparent;
}}

#topSearch {{
    background-color: {surface_2};
    color: {text};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0 12px 0 36px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
    font-size: 13px;
}}
#topSearch:focus {{
    border-color: {accent};
    background-color: {surface};
}}

#topSearchIcon {{
    color: {text_faint};
    background: transparent;
    qproperty-alignment: AlignCenter;
}}

#topIconBtn {{
    background: transparent;
    color: {text_dim};
    border: 1px solid transparent;
    border-radius: 8px;
}}
#topIconBtn:hover {{
    background-color: {surface_2};
    color: {text};
}}

#themeCombo {{
    background-color: {surface_2};
    color: {text};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0 12px;
    min-width: 130px;
}}
#themeCombo:hover {{
    background-color: {surface};
    border-color: {border_strong};
}}
#themeCombo:focus {{
    border-color: {accent};
}}
#themeCombo::drop-down {{
    border: none;
    width: 24px;
}}
#themeCombo QAbstractItemView {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
    outline: 0;
}}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR
   ═══════════════════════════════════════════════════════════ */
#sidebar {{
    background-color: {surface};
    border-right: 1px solid {border};
}}

#sidebarSearch {{
    background-color: {surface_2};
    color: {text};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0 12px;
    margin: 4px 8px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
}}
#sidebarSearch:focus {{
    border-color: {accent};
    background-color: {surface};
}}

#sidebarSectionLabel {{
    color: {text_faint};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 16px 14px 8px;
    background: transparent;
}}

#sidebarHomeBtn {{
    background-color: {surface_2};
    color: {text};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 0 12px;
    text-align: left;
    font-weight: 500;
    font-size: 13px;
    min-height: 36px;
}}
#sidebarHomeBtn:hover {{
    background-color: {accent_soft_bg};
    color: {accent_soft_fg};
    border-color: {accent_soft};
}}
#sidebarHomeBtn:pressed {{
    background-color: {surface_2};
}}

QTreeWidget {{
    background-color: transparent;
    border: none;
    color: {text};
    outline: 0;
    show-decoration-selected: 0;
}}
QTreeWidget::item {{
    padding: 6px 14px;
    border-radius: 6px;
    color: {text_dim};
    border: none;
    margin: 1px 8px;
}}
QTreeWidget::item:hover {{
    background-color: {surface_2};
    color: {text};
}}
QTreeWidget::item:selected {{
    background-color: {accent_soft_bg};
    color: {accent_soft_fg};
}}
QTreeWidget::branch {{
    background: transparent;
}}
QTreeWidget::branch:has-children {{
    /* default branch indicator — we hide it */
    image: none;
}}

/* Category headers (BOLD menu-style). We also set the font directly on
   each top-level QTreeWidgetItem in Python (the :has-children selector
   is unreliable in PyQt6). This QSS provides the padding/color fallback. */
QTreeWidget::item:has-children {{
    color: {text};
    padding-top: 14px;
    padding-bottom: 8px;
    font-size: 12px;
}}

/* ═══════════════════════════════════════════════════════════
   MAIN / CONTENT AREA
   ═══════════════════════════════════════════════════════════ */
#mainArea {{
    background-color: {bg};
}}

/* ═══════════════════════════════════════════════════════════
   PAGE HEADER (used inside every tool page)
   ═══════════════════════════════════════════════════════════ */
#pageHeader {{
    background: transparent;
}}

#breadcrumb {{
    color: {text_faint};
    font-size: 12px;
    background: transparent;
    padding: 0;
    margin-bottom: 6px;
}}
#breadcrumbCurrent {{
    color: {text};
    font-weight: 500;
}}

#pageTitle {{
    color: {text};
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: transparent;
    padding: 0;
}}
#pageSubtitle {{
    color: {text_dim};
    font-size: 14px;
    background: transparent;
    padding: 0;
    margin-top: 2px;
}}

#pageActions {{
    background: transparent;
}}

/* ═══════════════════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════════════════ */
QPushButton {{
    background-color: {surface_2};
    color: {text};
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0 14px;
    min-height: 34px;
    font-size: 13px;
    font-weight: 500;
    text-align: center;
}}
QPushButton:hover {{
    background-color: {surface};
    border-color: {border_strong};
}}
QPushButton:pressed {{
    background-color: {surface_2};
}}
QPushButton:disabled {{
    color: {text_faint};
}}

#btnPrimary {{
    background-color: {accent};
    color: {accent_fg};
    border: 1px solid {accent};
    font-weight: 600;
    min-height: 38px;
    padding: 0 16px;
    font-size: 13px;
}}
#btnPrimary:hover {{
    background-color: {accent_soft};
    border-color: {accent_soft};
}}
#btnPrimary:pressed {{
    background-color: {accent};
}}

/* Process / execute buttons — same look as btnPrimary, so all tools
   that use #executeBtn pick up the same accent treatment. */
#executeBtn {{
    background-color: {accent};
    color: {accent_fg};
    border: 1px solid {accent};
    border-radius: 8px;
    padding: 0 16px;
    min-height: 38px;
    font-size: 13px;
    font-weight: 600;
    text-align: center;
}}
#executeBtn:hover {{
    background-color: {accent_soft};
    border-color: {accent_soft};
    color: {accent_fg};
}}
#executeBtn:pressed {{
    background-color: {accent};
    color: {accent_fg};
}}

#btnSecondary {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border_strong};
}}
#btnSecondary:hover {{
    background-color: {surface_2};
    border-color: {border_strong};
}}

#btnGhost {{
    background-color: transparent;
    color: {text_dim};
    border: 1px solid transparent;
}}
#btnGhost:hover {{
    background-color: {surface_2};
    color: {text};
}}

#btnDangerGhost {{
    background-color: transparent;
    color: {danger};
    border: 1px solid transparent;
}}
#btnDangerGhost:hover {{
    background-color: {surface_2};
}}

#btnLink {{
    background: transparent;
    color: {accent};
    border: none;
    padding: 0;
    min-height: 0;
    text-align: left;
}}
#btnLink:hover {{
    color: {accent_soft};
    text-decoration: underline;
}}

/* ═══════════════════════════════════════════════════════════
   INPUTS
   ═══════════════════════════════════════════════════════════ */
QLineEdit, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QComboBox {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 0 12px;
    min-height: 34px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QDateTimeEdit:focus {{
    border-color: {accent};
}}
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled {{
    color: {text_faint};
    background-color: {surface_2};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0; height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {text_dim};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
    outline: 0;
}}

QPlainTextEdit {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 10px;
    padding: 12px;
    selection-background-color: {accent_soft_bg};
    selection-color: {accent_soft_fg};
    font-family: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
    font-size: 12.5px;
    line-height: 1.6;
}}
QPlainTextEdit:focus {{
    border-color: {accent};
}}
QPlainTextEdit[readOnly="true"] {{
    background-color: {surface_2};
    color: {text_dim};
}}

/* ═══════════════════════════════════════════════════════════
   LABELS
   ═══════════════════════════════════════════════════════════ */
QLabel {{
    color: {text_dim};
    background: transparent;
    padding: 0;
}}

#fieldLabel {{
    color: {text_dim};
    font-size: 12px;
    font-weight: 500;
    background: transparent;
}}
#fieldHint {{
    color: {text_faint};
    font-size: 11px;
    background: transparent;
}}

/* ═══════════════════════════════════════════════════════════
   CARDS
   ═══════════════════════════════════════════════════════════ */
#card {{
    background-color: {surface};
    border: 1px solid {border};
    border-radius: 12px;
}}

#cardHover {{
    background-color: {surface};
    border: 1px solid {border};
    border-radius: 12px;
}}
#cardHover:hover {{
    border-color: {accent_soft};
}}

#cardPrimary {{
    background-color: {surface};
    border: 1px solid {border};
    border-radius: 12px;
}}
#cardPrimary:hover {{
    border-color: {accent};
}}

/* ═══════════════════════════════════════════════════════════
   IO SECTION (input/output panels in tools)
   ═══════════════════════════════════════════════════════════ */
#ioHeader {{
    color: {text_dim};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: transparent;
    padding: 0;
}}
#ioHint {{
    color: {text_faint};
    font-size: 11px;
    background: transparent;
    padding: 0;
}}
#ioCount {{
    color: {text_faint};
    font-size: 11px;
    background: transparent;
    padding: 0;
}}

#ioIconBtn {{
    background: transparent;
    color: {text_faint};
    border: 1px solid transparent;
    border-radius: 6px;
    min-width: 28px;
    min-height: 28px;
    padding: 0;
}}
#ioIconBtn:hover {{
    background-color: {surface_2};
    color: {text};
}}

/* ═══════════════════════════════════════════════════════════
   WELCOME / DASHBOARD
   ═══════════════════════════════════════════════════════════ */
#welcomeEyebrow {{
    background-color: {accent_soft_bg};
    color: {accent_soft_fg};
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
}}
#welcomeTitle {{
    color: {text};
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: transparent;
    padding: 0;
    line-height: 1.15;
}}
#welcomeAccent {{
    color: {accent};
}}
#welcomeSub {{
    color: {text_dim};
    font-size: 15px;
    background: transparent;
    padding: 0;
}}
#sectionTitle {{
    color: {text_faint};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: transparent;
    padding: 0;
}}

#toolCardIcon {{
    background-color: {accent_soft_bg};
    color: {accent};
    border-radius: 8px;
    qproperty-alignment: AlignCenter;
    font-size: 16px;
    font-weight: 700;
}}
#toolCardTitle {{
    color: {text};
    font-size: 14px;
    font-weight: 600;
    background: transparent;
    padding: 0;
}}
#toolCardDesc {{
    color: {text_dim};
    font-size: 12px;
    background: transparent;
    padding: 0;
}}
#toolCardMeta {{
    color: {text_faint};
    font-size: 11px;
    background: transparent;
    padding: 0;
}}

#tag {{
    background-color: {surface_2};
    color: {text_dim};
    border-radius: 999px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 500;
}}

#statNum {{
    color: {text};
    font-size: 24px;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: transparent;
    padding: 0;
}}
#statLabel {{
    color: {text_faint};
    font-size: 12px;
    background: transparent;
    padding: 0;
}}

#kbd {{
    font-family: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
    font-size: 11px;
    color: {text_dim};
    background-color: {surface_2};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 1px 6px;
}}

/* ═══════════════════════════════════════════════════════════
   STATUS BAR (bottom)
   ═══════════════════════════════════════════════════════════ */
#statusBar {{
    background-color: {surface};
    border-top: 1px solid {border};
    color: {text_dim};
    font-size: 11px;
}}
#statusBar QLabel {{
    color: {text_dim};
    font-size: 11px;
    background: transparent;
    padding: 0 8px;
}}
#statusBar #statusReady {{
    color: {text};
    font-weight: 500;
}}

#statusDot {{
    background-color: {success};
    border-radius: 4px;
    min-width: 8px;
    max-width: 8px;
    min-height: 8px;
    max-height: 8px;
}}

/* ═══════════════════════════════════════════════════════════
   CHECKBOXES & RADIOS
   ═══════════════════════════════════════════════════════════ */
QCheckBox {{
    color: {text_dim};
    spacing: 8px;
    background: transparent;
    padding: 2px 0;
}}
QCheckBox:hover {{
    color: {text};
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {border_strong};
    border-radius: 4px;
    background-color: {surface};
}}
QCheckBox::indicator:hover {{
    border-color: {accent};
}}
QCheckBox::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}
QCheckBox::indicator:disabled {{
    border-color: {border};
    background-color: {surface_2};
}}

QRadioButton {{
    color: {text_dim};
    spacing: 8px;
    background: transparent;
    padding: 2px 0;
}}
QRadioButton:hover {{
    color: {text};
}}
QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border: 1.5px solid {border_strong};
    border-radius: 9px;
    background-color: {surface};
}}
QRadioButton::indicator:hover {{
    border-color: {accent};
}}
QRadioButton::indicator:checked {{
    background-color: {surface};
    border: 5px solid {accent};
}}

/* ═══════════════════════════════════════════════════════════
   GROUP BOX
   ═══════════════════════════════════════════════════════════ */
QGroupBox {{
    background-color: {surface};
    border: 1px solid {border};
    border-radius: 12px;
    margin-top: 16px;
    padding: 16px 12px 12px;
    font-weight: 600;
    color: {text};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: {text_dim};
    background-color: {surface};
}}

/* ═══════════════════════════════════════════════════════════
   SCROLLBARS
   ═══════════════════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 4px 2px;
}}
QScrollBar::handle:vertical {{
    background: {border_strong};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {accent};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    background: none;
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 2px 4px;
}}
QScrollBar::handle:horizontal {{
    background: {border_strong};
    border-radius: 5px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {accent};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    background: none;
    width: 0;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ═══════════════════════════════════════════════════════════
   SPLITTER
   ═══════════════════════════════════════════════════════════ */
QSplitter::handle {{
    background-color: {border};
}}
QSplitter::handle:vertical {{
    height: 1px;
}}
QSplitter::handle:horizontal {{
    width: 1px;
}}
QSplitter::handle:hover {{
    background-color: {accent};
}}

/* ═══════════════════════════════════════════════════════════
   MENUS
   ═══════════════════════════════════════════════════════════ */
QMenu {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{
    background-color: transparent;
    padding: 6px 16px;
    border-radius: 4px;
    margin: 1px 2px;
}}
QMenu::item:selected {{
    background-color: {accent_soft_bg};
    color: {accent_soft_fg};
}}
QMenu::separator {{
    height: 1px;
    background: {border};
    margin: 4px 8px;
}}

/* ═══════════════════════════════════════════════════════════
   TOOLTIPS
   ═══════════════════════════════════════════════════════════ */
QToolTip {{
    background-color: {surface};
    color: {text};
    border: 1px solid {border};
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
}}
"""


# ──────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ──────────────────────────────────────────────────────────────────────
def normalize_theme_name(theme_name: str) -> str:
    """Resolve a saved theme name, migrating old aliases to the current name."""
    if theme_name in PALETTES:
        return theme_name
    return THEME_ALIASES.get(theme_name, default_theme())


def get_theme_qss(theme_name: str) -> str:
    """Generate the complete QSS for a given theme (with alias migration)."""
    name = normalize_theme_name(theme_name)
    palette = PALETTES.get(name, PALETTES[default_theme()])
    return QSS_TEMPLATE.format(**palette)


def default_theme() -> str:
    return "Dark"
