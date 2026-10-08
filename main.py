"""
Text Manipulation Tools — Main Application
Modern minimal redesign.

Structure:
  ┌─ topBar (brand + global search + theme + global actions) ─┐
  │ sidebar  │  mainArea (page header + stacked content)       │
  ├──────────┴────────────────────────────────────────────────┤
  │ statusBar (theme / version / status)                      │
  └────────────────────────────────────────────────────────────┘
"""

import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QLineEdit, QLabel,
    QSplitter, QGraphicsOpacityEffect, QFrame, QGridLayout, QPushButton,
    QComboBox, QScrollArea, QStatusBar, QSizePolicy, QFileDialog, QSpacerItem,
    QStyle
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal, QSettings
from PyQt6.QtGui import QIcon, QFont, QColor, QMouseEvent

# ── Ensure project root is on sys.path ──────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from global_state import GlobalState
from theme_manager import PALETTES, get_theme_qss, default_theme, normalize_theme_name
import version as app_version

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ── Category imports (unchanged) ───────────────────────────────────
from tools.basic_text_tools import (
    AddPrefixSuffixTool, AddRemoveLineBreaksTool, AddRepeatsTool,
    CountCharsTool, SplitTextTool, FindReplaceTool,
    LetterCaseConverterTool, JoinMergeTextTool, RemoveDuplicateLinesTool,
    RemoveDuplicateWordsTool, RemoveEmptyLinesTool, RemoveExtraSpacesTool,
    RemoveLetterAccentsTool, RemoveLinesContainingTool, RemovePunctuationTool,
    SortTextLinesTool, RemoveLineNumbersTool, AlphabetizeTextTool
)
from tools.extraction_tools import (
    ExtractBetweenStringsTool, WordFrequencyCounterTool
)
from tools.format_web_tools import (
    AsciiUnicodeConverterTool, ConvertTimestampTool, DiffCheckerTool,
    RegexTesterTool, HexEncoderDecoderTool
)
from tools.obfuscation_tools import (
    BinaryTranslatorTool, Base64EncoderTool, DisemvowelTool,
    ReverseTextTool, ROT13Tool, WordScramblerTool
)
from tools.randomization_tools import (
    RandomLinePickerTool, RandomNumberGeneratorTool,
    RandomStringGeneratorTool, StringRandomizerTool
)
from tools.combination_tools import (
    CombinationGeneratorTool, ListsComparisonTool,
    LineCombinationGeneratorTool, PermutationGeneratorTool
)
from tools.numeration_tools import (
    GenerateNumberListTool, NumberEachLineTool, TallyCounterTool
)
from tools.allinone_tools import TextManipulationNotepadTool


# ═══════════════════════════════════════════════════════════════════════
#  Tool Registry  —  { "Category": [("Tool Name", WidgetClass), …] }
# ═══════════════════════════════════════════════════════════════════════
TOOL_REGISTRY: dict[str, list[tuple[str, type]]] = {
    "Basic Text Tools": [
        ("Add Prefix / Suffix / Delimiter", AddPrefixSuffixTool),
        ("Add / Remove Line Breaks", AddRemoveLineBreaksTool),
        ("Add Repeats", AddRepeatsTool),
        ("Count Characters, Words, etc.", CountCharsTool),
        ("Split Text by Delimiter", SplitTextTool),
        ("Find and Replace Text", FindReplaceTool),
        ("Letter Case Converter", LetterCaseConverterTool),
        ("Join / Merge Text (Line by Line)", JoinMergeTextTool),
        ("Remove Duplicate Lines", RemoveDuplicateLinesTool),
        ("Remove Duplicate Words", RemoveDuplicateWordsTool),
        ("Remove Empty Lines", RemoveEmptyLinesTool),
        ("Remove Extra Spaces", RemoveExtraSpacesTool),
        ("Remove Letter Accents", RemoveLetterAccentsTool),
        ("Remove Lines Containing", RemoveLinesContainingTool),
        ("Remove Punctuation", RemovePunctuationTool),
        ("Sort Text Lines", SortTextLinesTool),
        ("Remove Line Numbers", RemoveLineNumbersTool),
        ("Alphabetize Text", AlphabetizeTextTool),
    ],
    "Extraction & Analysis": [
        ("Extract Text Between Strings", ExtractBetweenStringsTool),
        ("Word Frequency Counter", WordFrequencyCounterTool),
    ],
    "Format & Web Tools": [
        ("ASCII / Unicode Converter", AsciiUnicodeConverterTool),
        ("Convert Timestamp", ConvertTimestampTool),
        ("Diff Checker (Text Compare)", DiffCheckerTool),
        ("Regex Tester / Matcher", RegexTesterTool),
        ("Hex Encoder / Decoder", HexEncoderDecoderTool),
    ],
    "Obfuscation & Encoding": [
        ("Binary Code Translator", BinaryTranslatorTool),
        ("Base64 Encode / Decode", Base64EncoderTool),
        ("Disemvowel Tool", DisemvowelTool),
        ("Reverse Text", ReverseTextTool),
        ("ROT13 Cipher", ROT13Tool),
        ("Word Scrambler", WordScramblerTool),
    ],
    "Randomization Tools": [
        ("Random Line Picker", RandomLinePickerTool),
        ("Random Number Generator", RandomNumberGeneratorTool),
        ("Random String Generator", RandomStringGeneratorTool),
        ("String Randomizer", StringRandomizerTool),
    ],
    "Combination / Permutation": [
        ("Combination Generator (nCk)", CombinationGeneratorTool),
        ("Lists Comparison Tool", ListsComparisonTool),
        ("Line Combination Generator", LineCombinationGeneratorTool),
        ("Permutation Generator (n!)", PermutationGeneratorTool),
    ],
    "Numeration Tools": [
        ("Generate List of Numbers", GenerateNumberListTool),
        ("Number Each Line", NumberEachLineTool),
        ("Online Tally Counter", TallyCounterTool),
    ],
    "All-in-One": [
        ("Text Manipulation Notepad", TextManipulationNotepadTool),
    ],
}

CATEGORY_ICONS = {
    "Basic Text Tools": "🔤",
    "Extraction & Analysis": "🔍",
    "Format & Web Tools": "🌐",
    "Obfuscation & Encoding": "🔒",
    "Randomization Tools": "🎲",
    "Combination / Permutation": "🔀",
    "Numeration Tools": "🔢",
    "All-in-One": "📝",
}


def category_for_tool(tool_name: str) -> str | None:
    for cat, tools in TOOL_REGISTRY.items():
        for tname, _ in tools:
            if tname == tool_name:
                return cat
    return None


# Welcome-card metadata for popular tools (short name, category label, icon, etc.)
TOOL_INFO: dict[str, dict] = {
    "Find and Replace Text":          {"short": "Find & Replace",   "cat": "Basic Text",   "icon": "🔎"},
    "Sort Text Lines":                 {"short": "Sort Lines",       "cat": "Basic Text",   "icon": "⇅"},
    "Base64 Encode / Decode":          {"short": "Base64",           "cat": "Encoding",     "icon": "⚙"},
    "Word Frequency Counter":          {"short": "Word Frequency",   "cat": "Analysis",     "icon": "Σ"},
    "Text Manipulation Notepad":       {"short": "Notepad",          "cat": "All-in-One",   "icon": "📝"},
    "Remove Duplicate Lines":          {"short": "Dedupe Lines",     "cat": "Basic Text",   "icon": "≡"},
    "Remove Empty Lines":              {"short": "Strip Empty",      "cat": "Basic Text",   "icon": "↳"},
    "Add Prefix / Suffix / Delimiter": {"short": "Prefix / Suffix",  "cat": "Basic Text",   "icon": "±"},
    "Letter Case Converter":           {"short": "Change Case",      "cat": "Basic Text",   "icon": "Aa"},
    "ROT13 Cipher":                    {"short": "ROT13",            "cat": "Encoding",     "icon": "↻"},
    "Reverse Text":                    {"short": "Reverse",          "cat": "Encoding",     "icon": "⇄"},
    "Remove Extra Spaces":             {"short": "Tidy Spaces",      "cat": "Basic Text",   "icon": "_"},
    "Count Characters, Words, etc.":   {"short": "Text Stats",       "cat": "Analysis",     "icon": "#"},
    "Add / Remove Line Breaks":        {"short": "Line Breaks",      "cat": "Basic Text",   "icon": "↵"},
    "Join / Merge Text (Line by Line)":{"short": "Merge",            "cat": "Basic Text",   "icon": "⊕"},
    "Split Text by Delimiter":                {"short": "Split Text by Delimiter", "cat": "Basic Text",   "icon": "▥"},
    "Remove Punctuation":              {"short": "Strip Punct.",     "cat": "Basic Text",   "icon": "∅"},
    "Alphabetize Text":                {"short": "Alphabetize",      "cat": "Basic Text",   "icon": "ABC"},
    "Random Line Picker":              {"short": "Random Line",      "cat": "Random",       "icon": "🎯"},
    "Random String Generator":         {"short": "Random String",    "cat": "Random",       "icon": "✱"},
    "Random Number Generator":         {"short": "Random Number",    "cat": "Random",       "icon": "#"},
    "Regex Tester / Matcher":          {"short": "Regex",            "cat": "Format",       "icon": ".*"},
    "Diff Checker (Text Compare)":     {"short": "Diff",             "cat": "Format",       "icon": "≠"},
    "Hex Encoder / Decoder":           {"short": "Hex",              "cat": "Format",       "icon": "0x"},
    "ASCII / Unicode Converter":       {"short": "ASCII ⇄ Unicode",  "cat": "Format",       "icon": "Ω"},
    "Convert Timestamp":               {"short": "Timestamp",        "cat": "Format",       "icon": "⏱"},
    "Extract Text Between Strings":    {"short": "Extract Between",  "cat": "Extraction",   "icon": "↔"},
    "Number Each Line":                {"short": "Number Lines",     "cat": "Numeration",   "icon": "№"},
    "Generate List of Numbers":        {"short": "Number List",      "cat": "Numeration",   "icon": "₁₂₃"},
    "Tally Counter":                   {"short": "Tally",            "cat": "Numeration",   "icon": "✓"},
    "Online Tally Counter":            {"short": "Tally",            "cat": "Numeration",   "icon": "✓"},
}


# ═══════════════════════════════════════════════════════════════════════
#  Welcome Dashboard
# ═══════════════════════════════════════════════════════════════════════
class ClickableCard(QFrame):
    """Tappable card on the welcome dashboard."""
    clicked = pyqtSignal(str)

    def __init__(self, name, category, description, target_tool, icon="✦", parent=None):
        super().__init__(parent)
        self.target_tool = target_tool
        self.setObjectName("cardHover")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        cl = QVBoxLayout(self)
        cl.setContentsMargins(20, 18, 20, 18)
        cl.setSpacing(8)

        # Icon tile
        icon_lbl = QLabel(icon)
        icon_lbl.setObjectName("toolCardIcon")
        icon_lbl.setFixedSize(36, 36)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cl.addWidget(icon_lbl)

        n_lbl = QLabel(name)
        n_lbl.setObjectName("toolCardTitle")
        cl.addWidget(n_lbl)

        c_lbl = QLabel(category)
        c_lbl.setObjectName("toolCardMeta")
        cl.addWidget(c_lbl)

        d_lbl = QLabel(description)
        d_lbl.setObjectName("toolCardDesc")
        d_lbl.setWordWrap(True)
        cl.addWidget(d_lbl)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.target_tool)
        super().mousePressEvent(event)


class WelcomeDashboard(QWidget):
    toolRequested = pyqtSignal(str)
    themeRequested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Outer: vertical layout to host a scroll area
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Scrollable container so it adapts to small windows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ── Hero ─────────────────────────────────────────────────
        hero = QVBoxLayout()
        hero.setSpacing(12)
        hero.setAlignment(Qt.AlignmentFlag.AlignCenter)

        eyebrow_row = QHBoxLayout()
        eyebrow_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eyebrow = QLabel("⚡  Quick start")
        self.eyebrow.setObjectName("welcomeEyebrow")
        self.eyebrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        eyebrow_row.addWidget(self.eyebrow)
        hero.addLayout(eyebrow_row)

        self.hero_title_1 = QLabel("Everything you need to")
        self.hero_title_1.setObjectName("welcomeTitle")
        self.hero_title_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(self.hero_title_1)

        self.hero_title_2 = QLabel()
        self.hero_title_2.setObjectName("welcomeTitle")
        self.hero_title_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hero_title_2.setTextFormat(Qt.TextFormat.RichText)
        self._render_hero_title_2()
        hero.addWidget(self.hero_title_2)

        # Compute tool count from the registry so it stays in sync
        # (and is computed before this welcome UI is built)
        tool_count = sum(len(tools) for tools in TOOL_REGISTRY.values())
        cat_count = len(TOOL_REGISTRY)

        self.hero_sub = QLabel(
            f"A complete toolbox for transforming, cleaning, and analyzing text — "
            f"{tool_count} tools across {cat_count} categories, ready when you are."
        )
        self.hero_sub.setObjectName("welcomeSub")
        self.hero_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hero_sub.setWordWrap(True)
        self.hero_sub.setMaximumWidth(620)
        hero.addWidget(self.hero_sub, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(hero)
        layout.addSpacing(40)

        # ── Frequently used (most-used tools) ──────────────────
        layout.addWidget(self._section_title("FREQUENTLY USED"))
        layout.addSpacing(12)
        # A container that we rebuild on every refresh
        self.freq_used_container = QWidget()
        self.freq_used_layout = QVBoxLayout(self.freq_used_container)
        self.freq_used_layout.setContentsMargins(0, 0, 0, 0)
        self.freq_used_layout.setSpacing(0)
        layout.addWidget(self.freq_used_container)
        layout.addSpacing(32)

        # ── Featured tools (curated picks) ──────────────────────
        layout.addWidget(self._section_title("FEATURED TOOLS"))
        layout.addSpacing(12)

        cards_data = [
            ("Find & Replace",      "Basic Text",      "Search and replace with regex support.",            "Find and Replace Text",          "🔎"),
            ("Sort Text Lines",     "Basic Text",      "Sort alphabetically, numerically, or by length.",   "Sort Text Lines",                "⇅"),
            ("Base64",              "Encoding",        "Encode or decode Base64 strings instantly.",        "Base64 Encode / Decode",         "⚙"),
            ("Word Frequency",      "Analysis",        "Count and rank word usage in your text.",           "Word Frequency Counter",         "Σ"),
        ]
        grid = QGridLayout()
        grid.setSpacing(16)
        for i, (name, cat, desc, target, icon) in enumerate(cards_data):
            card = ClickableCard(name, cat, desc, target, icon)
            card.clicked.connect(self.toolRequested.emit)
            grid.addWidget(card, i // 2, i % 2)
        layout.addLayout(grid)
        layout.addSpacing(32)

        # ── Stats row ────────────────────────────────────────────
        layout.addWidget(self._section_title("AT A GLANCE"))
        layout.addSpacing(12)

        stats = QHBoxLayout()
        stats.setSpacing(16)

        def stat_card(num, label, desc):
            c = QFrame()
            c.setObjectName("card")
            v = QVBoxLayout(c)
            v.setContentsMargins(20, 16, 20, 16)
            v.setSpacing(4)
            row = QHBoxLayout()
            row.setSpacing(8)
            row.setAlignment(Qt.AlignmentFlag.AlignBaseline)
            n = QLabel(num)
            n.setObjectName("statNum")
            l = QLabel(label)
            l.setObjectName("statLabel")
            row.addWidget(n)
            row.addWidget(l, 1)
            v.addLayout(row)
            d = QLabel(desc)
            d.setObjectName("toolCardDesc")
            d.setWordWrap(True)
            v.addWidget(d)
            return c

        stats.addWidget(stat_card(str(tool_count), "tools", f"Across {cat_count} categories — from basic transforms to analysis."))
        stats.addWidget(stat_card("18", "formats", "Drop .txt, .csv, .json, .md, .log and more directly onto any input."))
        stats.addWidget(stat_card("∞", "chained", "Pipe results from one tool into the next without copy-paste."))
        layout.addLayout(stats)
        layout.addSpacing(32)

        # ── Tips ─────────────────────────────────────────────────
        layout.addWidget(self._section_title("GET THE MOST OUT OF IT"))
        layout.addSpacing(12)

        tips = QFrame()
        tips.setObjectName("card")
        tv = QVBoxLayout(tips)
        tv.setContentsMargins(20, 12, 20, 12)
        tv.setSpacing(0)

        tips_data = [
            ("🔎",  "Search any tool",  "Type in the top bar to filter the tool list.",         None),
            ("⏪",  "Chain tools",      "Use Last Result pulls the previous tool's output into the current one.", None),
            ("📋",  "Notepad",          "Use Notepad moves your scratchpad text into the current input.",      None),
            ("🎨",  "Switch themes",    "Pick a theme — Daylight, Snow, Sunset, Blush, or Forest.", None),
        ]
        for icon, name, desc, _ in tips_data:
            row = QHBoxLayout()
            row.setSpacing(14)
            row.setContentsMargins(0, 10, 0, 10)

            ic = QLabel(icon)
            ic.setObjectName("toolCardIcon")
            ic.setFixedSize(32, 32)
            ic.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(ic)

            n = QLabel(name)
            n.setObjectName("toolCardTitle")
            row.addWidget(n)

            d = QLabel(desc)
            d.setObjectName("toolCardDesc")
            row.addWidget(d, 1)

            tv.addLayout(row)

        layout.addWidget(tips)
        layout.addStretch()

    def _section_title(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setObjectName("sectionTitle")
        return l

    # ── Frequently Used: rebuild from usage counts ────────────
    def refresh_frequently_used(self, settings, registry):
        """Read tool usage counts from QSettings and rebuild the section."""
        counts: list[tuple[str, int]] = []
        for _cat, tools in registry.items():
            for tname, _ in tools:
                try:
                    c = int(settings.value(f"toolUsage/{tname}", 0))
                except (TypeError, ValueError):
                    c = 0
                if c > 0:
                    counts.append((tname, c))
        counts.sort(key=lambda x: -x[1])
        self._render_frequently_used(counts[:4])

    def _render_frequently_used(self, top_tools: list[tuple[str, int]]):
        # Clear current
        while self.freq_used_layout.count():
            item = self.freq_used_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        if not top_tools:
            # Empty state
            empty = QFrame()
            empty.setObjectName("card")
            ev = QVBoxLayout(empty)
            ev.setContentsMargins(24, 20, 24, 20)
            ev.setSpacing(4)
            h = QLabel("Nothing here yet")
            h.setObjectName("toolCardTitle")
            sub = QLabel("Use a few tools and your most-used ones will appear here automatically.")
            sub.setObjectName("toolCardDesc")
            sub.setWordWrap(True)
            ev.addWidget(h)
            ev.addWidget(sub)
            self.freq_used_layout.addWidget(empty)
            return

        grid = QGridLayout()
        grid.setSpacing(16)
        for i, (tname, c) in enumerate(top_tools):
            info = TOOL_INFO.get(tname, {})
            short_name = info.get("short", tname)
            cat = info.get("cat", "Tool")
            desc = f"Used {c} time{'s' if c != 1 else ''}."
            icon = info.get("icon", "✦")
            card = ClickableCard(short_name, cat, desc, tname, icon)
            card.clicked.connect(self.toolRequested.emit)
            grid.addWidget(card, i // 2, i % 2)
        self.freq_used_layout.addLayout(grid)

    def _render_hero_title_2(self):
        accent = "#D97706"  # safe amber default; updated on theme change
        self.hero_title_2.setText(
            f'<span style="color:{accent}; font-weight:800;">manipulate text</span>, fast.'
        )

    def apply_theme(self, palette: dict):
        """Refresh theme-dependent rich text (e.g., accent color in the hero)."""
        accent = palette.get("accent", "#D97706")
        self.hero_title_2.setText(
            f'<span style="color:{accent}; font-weight:800;">manipulate text</span>, fast.'
        )


# ═══════════════════════════════════════════════════════════════════════
#  Main Window
# ═══════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{app_version.__app_name__} v{app_version.__version__}")
        self.setMinimumSize(960, 640)
        self._state = GlobalState()
        self.settings = QSettings(app_version.__app_org__, app_version.__app_name__)
        self._tool_widgets: dict[str, QWidget] = {}
        self._tree_items: dict[str, QTreeWidgetItem] = {}
        self._cat_items: dict[str, QTreeWidgetItem] = {}
        self._current_anim = None
        self._current_tool: str | None = None
        self._current_theme: str = default_theme()
        self._style = QApplication.instance().style()

        # Set window icon
        icon_path = resource_path("icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Restore window geometry (size + position) from previous run
        self._restore_window_geometry()

        self._build_ui()
        self._populate_sidebar()
        self._build_statusbar()

        # Show welcome by default and populate Frequently Used from existing usage
        self.welcome.refresh_frequently_used(self.settings, TOOL_REGISTRY)
        self.stack.setCurrentWidget(self.welcome)
        self._set_status_tool("Welcome")

    # ──────────────────────────────────────────── window geometry
    def _restore_window_geometry(self):
        size = self.settings.value("window/size")
        pos = self.settings.value("window/pos")
        maximized = self.settings.value("window/maximized", "false")
        if size:
            try:
                w, h = [int(x) for x in str(size).split(",")]
                self.resize(w, h)
            except (ValueError, AttributeError):
                self.resize(1280, 850)
        else:
            self.resize(1280, 850)
        if pos:
            try:
                x, y = [int(v) for v in str(pos).split(",")]
                self.move(x, y)
            except (ValueError, AttributeError):
                pass
        # If the window was maximized when last closed, restore that
        # state after the window is shown (defer to the event loop).
        if str(maximized).lower() == "true":
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, lambda: self.setWindowState(
                self.windowState() | Qt.WindowState.WindowMaximized
            ))

    def _save_window_geometry(self):
        # If the window is currently maximized, self.size() and self.pos()
        # return the maximized geometry (which is just the screen rect).
        # Use normalGeometry() instead so we save the size it WOULD have
        # when not maximized, so we can restore the user's preferred
        # window size when they next un-maximize.
        if self.isMaximized() or self.isFullScreen():
            geo = self.normalGeometry()
        else:
            geo = self.geometry()
        self.settings.setValue("window/size", f"{geo.width()},{geo.height()}")
        self.settings.setValue("window/pos", f"{geo.x()},{geo.y()}")
        self.settings.setValue("window/maximized", self.isMaximized())
        self.settings.sync()

    # ────────────────────────────────────────────────────── build UI
    def _build_ui(self):
        # Resolve saved theme, migrating any old name (e.g. "Snow" -> "Dark")
        saved_theme = self.settings.value("theme", default_theme())
        saved_theme = normalize_theme_name(saved_theme)
        self._current_theme = saved_theme
        # If the saved name was an old alias, persist the migrated name
        if saved_theme != self.settings.value("theme", ""):
            self.settings.setValue("theme", saved_theme)
            self.settings.sync()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Top bar
        root.addWidget(self._build_topbar())

        # Main row (sidebar + content)
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self._build_sidebar())
        body_layout.addWidget(self._build_main(), 1)
        root.addWidget(body, 1)

    # ─── Top bar
    def _build_topbar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("topBar")
        bar.setFixedHeight(60)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(20, 0, 20, 0)
        lay.setSpacing(14)

        # Brand
        brand = QHBoxLayout()
        brand.setSpacing(10)
        mark = QLabel("T")
        mark.setObjectName("brandMark")
        mark.setFixedSize(32, 32)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.addWidget(mark)
        name = QLabel("Text Mechanic")
        name.setObjectName("brandText")
        brand.addWidget(name)
        lay.addLayout(brand)

        lay.addSpacing(20)

        # Global search
        search_wrap = QWidget()
        search_wrap.setFixedHeight(36)
        search_lay = QHBoxLayout(search_wrap)
        search_lay.setContentsMargins(0, 0, 0, 0)
        search_lay.setSpacing(0)

        # icon overlay
        search_inner = QWidget()
        si = QHBoxLayout(search_inner)
        si.setContentsMargins(10, 0, 10, 0)
        si.setSpacing(8)

        search_icon = QLabel()
        search_icon.setObjectName("topSearchIcon")
        search_icon.setPixmap(self._style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView).pixmap(14, 14))
        search_icon.setFixedSize(16, 16)
        search_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        si.addWidget(search_icon)

        self.top_search = QLineEdit()
        self.top_search.setObjectName("topSearch")
        self.top_search.setPlaceholderText("Search tools…")
        self.top_search.setFixedHeight(36)
        self.top_search.textChanged.connect(self._filter_tree)
        # The placeholder icon overlay is just visual; line edit is full-width
        si.addWidget(self.top_search, 1)
        search_lay.addWidget(search_inner)

        # Use a fixed max width to keep the top bar tidy
        search_holder = QWidget()
        sh_lay = QHBoxLayout(search_holder)
        sh_lay.setContentsMargins(0, 0, 0, 0)
        sh_lay.addWidget(search_wrap)
        search_holder.setMaximumWidth(420)
        sh_lay.addStretch()
        lay.addWidget(search_holder, 1)

        lay.addStretch()

        # Global action buttons (Use Last Result, Use Notepad, Open File) with Qt icons
        self.top_btn_last = self._make_top_btn(
            QStyle.StandardPixmap.SP_BrowserReload,
            "Use Last Result (Ctrl+L)\nPulls the previous tool's output into the current input.",
            self._use_last_result,
        )
        self.top_btn_np = self._make_top_btn(
            QStyle.StandardPixmap.SP_FileIcon,
            "Use Notepad (Ctrl+N)\nMoves your scratchpad text into the current input.",
            self._use_notepad,
        )
        self.top_btn_open = self._make_top_btn(
            QStyle.StandardPixmap.SP_DirOpenIcon,
            "Open File (Ctrl+O)\nLoad a text file into the current tool's input.",
            self._open_global_file,
        )
        lay.addWidget(self.top_btn_last)
        lay.addWidget(self.top_btn_np)
        lay.addWidget(self.top_btn_open)

        # Divider (visual)
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setStyleSheet("color: rgba(127,127,127,0.25);")
        divider.setFixedHeight(24)
        lay.addSpacing(4)
        lay.addWidget(divider)
        lay.addSpacing(4)

        # Theme selector
        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("themeCombo")
        self.theme_combo.addItems(list(PALETTES.keys()))
        self.theme_combo.setCurrentText(self._current_theme)
        self.theme_combo.currentTextChanged.connect(self._change_theme)
        lay.addWidget(self.theme_combo)

        return bar

    def _make_top_btn(self, std_pixmap, tooltip: str, slot) -> QPushButton:
        b = QPushButton()
        b.setObjectName("topIconBtn")
        b.setIcon(self._style.standardIcon(std_pixmap))
        b.setIconSize(QSize(18, 18))
        b.setToolTip(tooltip)
        b.setFixedSize(36, 36)
        b.clicked.connect(slot)
        return b

    # ─── Sidebar
    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(264)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 12, 0, 12)
        sb.setSpacing(4)

        # Compute counts up front (TOOL_REGISTRY is module-level)
        _tool_count = sum(len(tools) for tools in TOOL_REGISTRY.values())
        _cat_count = len(TOOL_REGISTRY)

        # ── Home button (always-visible way back to the welcome dashboard)
        self.home_btn = QPushButton()
        self.home_btn.setObjectName("sidebarHomeBtn")
        self.home_btn.setIcon(self._style.standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon))
        self.home_btn.setIconSize(QSize(16, 16))
        self.home_btn.setText("  Home")
        self.home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.home_btn.setFixedHeight(36)
        home_wrap = QWidget()
        hw = QHBoxLayout(home_wrap)
        hw.setContentsMargins(8, 0, 8, 0)
        hw.addWidget(self.home_btn)
        sb.addWidget(home_wrap)
        self.home_btn.clicked.connect(self._go_home)

        # Section label
        section = QLabel("Tools")
        section.setObjectName("sidebarSectionLabel")
        sb.addWidget(section)

        # Sidebar-local search
        self.sidebar_search = QLineEdit()
        self.sidebar_search.setObjectName("sidebarSearch")
        self.sidebar_search.setPlaceholderText("Filter…")
        self.sidebar_search.setFixedHeight(34)
        self.sidebar_search.textChanged.connect(self._filter_tree)
        sb.addWidget(self.sidebar_search)

        # Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(0)
        self.tree.setRootIsDecorated(False)
        self.tree.setAnimated(True)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tree.currentItemChanged.connect(self._on_item_changed)
        self.tree.itemClicked.connect(self._on_item_clicked)
        sb.addWidget(self.tree, 1)

        # Footer note
        footer = QLabel(f"{_tool_count} tools · {_cat_count} categories")
        footer.setObjectName("sidebarSectionLabel")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.addWidget(footer)

        return sidebar

    def _go_home(self):
        """Switch the stack back to the welcome dashboard."""
        self.stack.setCurrentWidget(self.welcome)
        self.tree.clearSelection()
        self.tree.setCurrentItem(None)
        self._current_tool = None
        self._set_status_tool("Welcome")
        self._set_status("Ready")
        # Refresh Frequently Used with the latest usage counts
        self.welcome.refresh_frequently_used(self.settings, TOOL_REGISTRY)
        # Clear the search boxes too so the tree shows everything
        if self.sidebar_search.text():
            self.sidebar_search.clear()
        if self.top_search.text():
            self.top_search.clear()

    def _record_tool_use(self, tool_name: str):
        """Increment this tool's usage counter (persisted in QSettings)."""
        key = f"toolUsage/{tool_name}"
        try:
            current = int(self.settings.value(key, 0))
        except (TypeError, ValueError):
            current = 0
        self.settings.setValue(key, current + 1)
        self.settings.sync()

    # ─── Main area
    def _build_main(self) -> QWidget:
        main = QWidget()
        main.setObjectName("mainArea")
        lay = QVBoxLayout(main)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Scrollable content area so long tool pages can scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        lay.addWidget(scroll, 1)

        # The actual stacked content lives inside the scroll area
        scroll_host = QWidget()
        scroll.setWidget(scroll_host)
        host_lay = QVBoxLayout(scroll_host)
        host_lay.setContentsMargins(0, 0, 0, 0)
        host_lay.setSpacing(0)

        self.stack = QStackedWidget()
        host_lay.addWidget(self.stack)

        # Welcome
        self.welcome = WelcomeDashboard()
        self.welcome.toolRequested.connect(self._on_dashboard_request)
        self.stack.addWidget(self.welcome)

        return main

    # ─── Status bar
    def _build_statusbar(self):
        sb = QStatusBar()
        sb.setObjectName("statusBar")
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

        # Left: ready dot + status text
        self.status_dot = QLabel()
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedSize(8, 8)
        sb.addWidget(self.status_dot)

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusReady")
        sb.addWidget(self.status_label)

        # Spacer (fixed-width label) between left and right groups
        spacer = QLabel("")
        spacer.setFixedWidth(24)
        sb.addPermanentWidget(spacer)

        # Permanent: tool, theme, version
        self.status_tool_lbl = QLabel("Welcome")
        sb.addPermanentWidget(self.status_tool_lbl)

        sep1 = QLabel("·")
        sep1.setStyleSheet("color: rgba(127,127,127,0.4);")
        sb.addPermanentWidget(sep1)

        self.status_theme_lbl = QLabel(self._current_theme)
        sb.addPermanentWidget(self.status_theme_lbl)

        sep2 = QLabel("·")
        sep2.setStyleSheet("color: rgba(127,127,127,0.4);")
        sb.addPermanentWidget(sep2)

        version_lbl = QLabel(app_version.short_version_string())
        sb.addPermanentWidget(version_lbl)

    def _set_status(self, msg: str):
        self.status_label.setText(msg)

    def _set_status_tool(self, name: str):
        self.status_tool_lbl.setText(name)

    def _set_status_theme(self, name: str):
        self.status_theme_lbl.setText(name)

    # ──────────────────────────────────────────────── populate sidebar
    def _populate_sidebar(self):
        # Bold font for category headers (top-level items) — QSS :has-children
        # is unreliable in PyQt6, so we set the font directly on the item.
        cat_font = QFont()
        cat_font.setBold(True)
        cat_font.setPointSize(11)

        for cat_name, tools in TOOL_REGISTRY.items():
            icon = CATEGORY_ICONS.get(cat_name, "")
            cat_item = QTreeWidgetItem(self.tree, [f"{icon}  {cat_name}"])
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            cat_item.setFont(0, cat_font)
            cat_item.setExpanded(False)
            self._cat_items[cat_name] = cat_item

            for tool_name, _ in tools:
                child = QTreeWidgetItem(cat_item, [tool_name])
                child.setData(0, Qt.ItemDataRole.UserRole, tool_name)
                self._tree_items[tool_name] = child

        self._load_sidebar_state()

    def _load_sidebar_state(self):
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            for reg_name in TOOL_REGISTRY:
                if reg_name in item.text(0):
                    val = self.settings.value(f"Sidebar/{reg_name}/Expanded")
                    if val is not None:
                        item.setExpanded(str(val).lower() == "true")
                    break

    def _save_sidebar_state(self):
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            for reg_name in TOOL_REGISTRY:
                if reg_name in item.text(0):
                    self.settings.setValue(f"Sidebar/{reg_name}/Expanded", item.isExpanded())
                    break

    # ─────────────────────────────────────────── switching tools
    def _on_item_clicked(self, item: QTreeWidgetItem, _column):
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())

    def _on_item_changed(self, current: QTreeWidgetItem, _prev):
        if current is None:
            return
        name = current.data(0, Qt.ItemDataRole.UserRole)
        if name is None:
            return
        self._switch_to_tool(name)

    def _on_dashboard_request(self, tool_name: str):
        if tool_name in self._tree_items:
            item = self._tree_items[tool_name]
            self.tree.setCurrentItem(item)
            if item.parent():
                item.parent().setExpanded(True)

    def _switch_to_tool(self, name: str):
        if name not in self._tool_widgets:
            for _cat, tools in TOOL_REGISTRY.items():
                for tool_name, tool_cls in tools:
                    if tool_name == name:
                        widget = tool_cls()
                        # If the tool has an apply_theme hook, give it a chance now
                        if hasattr(widget, "apply_theme"):
                            widget.apply_theme(PALETTES.get(self._current_theme, {}))
                        self._tool_widgets[name] = widget
                        self.stack.addWidget(widget)
                        break

        if name in self._tool_widgets:
            self._fade_to_widget(self._tool_widgets[name])
            self._current_tool = name
            self._set_status_tool(name)
            self._set_status(f"Loaded: {name}")
            self._record_tool_use(name)

    def _fade_to_widget(self, target_widget):
        if self.stack.currentWidget() == target_widget:
            return

        eff = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(eff)

        self._anim = QPropertyAnimation(eff, b"opacity")
        self._anim.setDuration(140)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        def on_fade_out():
            self.stack.setCurrentWidget(target_widget)
            self._anim_in = QPropertyAnimation(eff, b"opacity")
            self._anim_in.setDuration(180)
            self._anim_in.setStartValue(0.0)
            self._anim_in.setEndValue(1.0)
            self._anim_in.setEasingCurve(QEasingCurve.Type.InQuad)
            self._anim_in.start()

        self._anim.finished.connect(on_fade_out)
        self._anim.start()

    # ─────────────────────────────────────────── Global Actions
    def _use_last_result(self):
        curr = self.stack.currentWidget()
        target = None
        if hasattr(curr, "input_text"):
            target = curr.input_text
        elif hasattr(curr, "notepad"):
            target = curr.notepad
        if target is not None:
            target.setPlainText(self._state.last_result)
            self._set_status("Applied: Last Result")

    def _use_notepad(self):
        curr = self.stack.currentWidget()
        target = None
        if hasattr(curr, "input_text"):
            target = curr.input_text
        elif hasattr(curr, "notepad"):
            target = curr.notepad
        if target is not None:
            target.setPlainText(self._state.notepad_text)
            self._set_status("Applied: Notepad Content")

    def _open_global_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "",
            "Text Files (*.txt *.csv *.log *.md *.json *.xml *.html *.ini "
            "*.cfg *.yaml *.yml *.tsv *.srt *.vtt *.py *.js *.css);;"
            "All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            curr = self.stack.currentWidget()
            target = None
            if hasattr(curr, "input_text"):
                target = curr.input_text
            elif hasattr(curr, "notepad"):
                target = curr.notepad
            if target is not None:
                target.setPlainText(content)
                self._set_status(f"Opened: {os.path.basename(path)}")
        except Exception as e:
            self._set_status(f"Error: {e}")

    def _change_theme(self, theme_name: str):
        if theme_name not in PALETTES:
            return
        self._current_theme = theme_name
        qss = get_theme_qss(theme_name)
        QApplication.instance().setStyleSheet(qss)
        self.settings.setValue("theme", theme_name)
        self._set_status_theme(theme_name)
        # Refresh theme-aware widgets
        if hasattr(self.welcome, "apply_theme"):
            self.welcome.apply_theme(PALETTES[theme_name])
        for widget in self._tool_widgets.values():
            if hasattr(widget, "apply_theme"):
                widget.apply_theme(PALETTES[theme_name])

    # ─────────────────────────────────────────── search / filter
    def _filter_tree(self, text: str):
        text = text.lower().strip()
        for i in range(self.tree.topLevelItemCount()):
            cat = self.tree.topLevelItem(i)
            any_visible = False
            for j in range(cat.childCount()):
                child = cat.child(j)
                match = text == "" or text in child.text(0).lower()
                child.setHidden(not match)
                if match:
                    any_visible = True
            cat.setHidden(not any_visible)
            if any_visible and text:
                cat.setExpanded(True)

    # ─────────────────────────────────────────── lifecycle
    def closeEvent(self, event):
        # Save tool settings
        for widget in self._tool_widgets.values():
            if hasattr(widget, "save_settings"):
                widget.save_settings()
        self._save_sidebar_state()
        self._save_window_geometry()
        super().closeEvent(event)


# ═══════════════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    # Make app metadata visible to the OS (helps with QSettings and taskbar)
    app.setApplicationName(app_version.__app_name__)
    app.setApplicationVersion(app_version.__version__)
    app.setOrganizationName(app_version.__app_org__)

    from theme_manager import get_theme_qss
    settings = QSettings(app_version.__app_org__, app_version.__app_name__)
    saved_theme = normalize_theme_name(settings.value("theme", default_theme()))
    app.setStyleSheet(get_theme_qss(saved_theme))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
