"""
Base widget for all text manipulation tools.

Provides a standardized layout:
  ┌─ Page header (breadcrumb · title · actions) ─┐
  │ Controls (subclass fills via build_controls)  │
  │ ┌─ Input card ─┐  ┌─ Output card ─┐         │
  │ │ header + …   │  │ header + …    │         │
  │ │ textarea     │  │ textarea (RO) │         │
  │ │ hint         │  │ hint / count  │         │
  │ └──────────────┘  └──────────────┘         │
  │ Action bar (Copy Result · Clear All)          │
  └────────────────────────────────────────────────┘

Subclasses override build_controls(layout) to insert tool-specific UI.
Optional helpers: set_breadcrumb, set_subtitle, add_page_action, add_io_action.
"""

import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QLabel, QApplication, QFileDialog,
    QLineEdit, QCheckBox, QSpinBox, QComboBox, QFrame
)
from PyQt6.QtCore import Qt, QMimeData, QSettings
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from global_state import GlobalState


class DroppableTextEdit(QPlainTextEdit):
    """QPlainTextEdit that accepts drag-and-drop of text files."""

    SUPPORTED_EXTENSIONS = {
        '.txt', '.csv', '.log', '.md', '.json', '.xml',
        '.html', '.htm', '.ini', '.cfg', '.yaml', '.yml',
        '.tsv', '.srt', '.vtt', '.py', '.js', '.css',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path) and self._is_text_file(path):
                    event.acceptProposedAction()
                    return
        super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            texts = []
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if os.path.isfile(path) and self._is_text_file(path):
                    try:
                        with open(path, 'r', encoding='utf-8', errors='replace') as f:
                            texts.append(f.read())
                    except Exception:
                        pass
            if texts:
                self.setPlainText("\n".join(texts))
                event.acceptProposedAction()
                return
        super().dropEvent(event)

    @staticmethod
    def _is_text_file(path: str) -> bool:
        _, ext = os.path.splitext(path)
        return ext.lower() in DroppableTextEdit.SUPPORTED_EXTENSIONS


class BaseToolWidget(QWidget):
    """
    Base class for tool pages. Provides a refined page header, IO section,
    and standard action bar. Subclasses override build_controls() to add
    their tool-specific controls (and may add page actions / IO actions).
    """

    DEFAULT_INPUT_PLACEHOLDER = (
        "Paste or type your text here, or drag & drop a .txt file…"
    )
    DEFAULT_OUTPUT_PLACEHOLDER = "Results appear here…"

    def __init__(self, title: str = "Tool", parent=None):
        super().__init__(parent)
        self._title = title
        self._state = GlobalState()
        self.settings = QSettings("Antigravity", "TextManipulationTools")
        self._build_ui()
        # load_settings must be called AFTER build_controls in subclasses
        # for safety we call it here too — it's idempotent
        self.load_settings()

    # ─────────────────────────────────────────────────────── hide event
    def hideEvent(self, event):
        self.save_settings()
        super().hideEvent(event)

    # ───────────────────────────────────────────────────── UI assembly
    def _build_ui(self):
        # Root
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 32, 36, 32)
        root.setSpacing(20)

        # 1) Page header ──────────────────────────────────────
        root.addWidget(self._build_page_header())

        # 2) Tool-specific controls (subclass fills this) ───
        self._controls_layout = QVBoxLayout()
        self._controls_layout.setSpacing(14)
        root.addLayout(self._controls_layout)
        self.build_controls(self._controls_layout)

        # 3) Input / Output cards (side by side) ───────────
        root.addWidget(self._build_io_section(), 1)

        # 4) Bottom action bar ───────────────────────────────
        root.addLayout(self._build_action_bar())

    def _build_page_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("pageHeader")
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Breadcrumb
        self._breadcrumb_lbl = QLabel("")
        self._breadcrumb_lbl.setObjectName("breadcrumb")
        self._breadcrumb_lbl.setVisible(False)
        layout.addWidget(self._breadcrumb_lbl)

        # Title row (title + actions)
        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(12)

        self._title_lbl = QLabel(self._title)
        self._title_lbl.setObjectName("pageTitle")
        title_row.addWidget(self._title_lbl)
        title_row.addStretch()

        # Actions container (subclass adds via add_page_action)
        self._page_actions = QWidget()
        self._page_actions.setObjectName("pageActions")
        pa_lay = QHBoxLayout(self._page_actions)
        pa_lay.setContentsMargins(0, 0, 0, 0)
        pa_lay.setSpacing(8)
        title_row.addWidget(self._page_actions)

        layout.addLayout(title_row)

        # Subtitle
        self._subtitle_lbl = QLabel("")
        self._subtitle_lbl.setObjectName("pageSubtitle")
        self._subtitle_lbl.setVisible(False)
        layout.addWidget(self._subtitle_lbl)

        return header

    def _build_io_section(self) -> QWidget:
        # Side-by-side: input card + output card
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(16)

        # ── Input card
        in_card = QFrame()
        in_card.setObjectName("card")
        in_lay = QVBoxLayout(in_card)
        in_lay.setContentsMargins(18, 14, 18, 16)
        in_lay.setSpacing(10)

        in_header = QHBoxLayout()
        in_header.setSpacing(8)
        in_title = QLabel("Input")
        in_title.setObjectName("ioHeader")
        in_header.addWidget(in_title)

        in_meta = QLabel("")
        in_meta.setObjectName("ioCount")
        in_header.addSpacing(6)
        in_header.addWidget(in_meta)
        in_header.addStretch()

        # Inline IO actions (subclass adds via add_io_action)
        self._in_actions = QHBoxLayout()
        self._in_actions.setContentsMargins(0, 0, 0, 0)
        self._in_actions.setSpacing(2)
        in_actions_w = QWidget()
        in_actions_w.setLayout(self._in_actions)
        in_header.addWidget(in_actions_w)
        in_lay.addLayout(in_header)

        self.input_text = DroppableTextEdit()
        self.input_text.setPlaceholderText(self.DEFAULT_INPUT_PLACEHOLDER)
        in_lay.addWidget(self.input_text, 1)

        in_hint = QLabel("⤵  Drag & drop a .txt, .csv, .json, .md, or .log file")
        in_hint.setObjectName("ioHint")
        in_lay.addWidget(in_hint)

        # We need to keep references to in_meta, in_hint for updates
        self._in_count_lbl = in_meta
        self._in_hint_lbl = in_hint

        # Wrap input card in a container so row can hold it + output card
        in_container = QWidget()
        in_container_lay = QVBoxLayout(in_container)
        in_container_lay.setContentsMargins(0, 0, 0, 0)
        in_container_lay.addWidget(in_card)
        row.addWidget(in_container, 1)

        # ── Output card
        out_card = QFrame()
        out_card.setObjectName("card")
        out_lay = QVBoxLayout(out_card)
        out_lay.setContentsMargins(18, 14, 18, 16)
        out_lay.setSpacing(10)

        out_header = QHBoxLayout()
        out_header.setSpacing(8)
        out_title = QLabel("Output")
        out_title.setObjectName("ioHeader")
        out_header.addWidget(out_title)

        out_meta = QLabel("")
        out_meta.setObjectName("ioCount")
        out_header.addSpacing(6)
        out_header.addWidget(out_meta)
        out_header.addStretch()

        self._out_actions = QHBoxLayout()
        self._out_actions.setContentsMargins(0, 0, 0, 0)
        self._out_actions.setSpacing(2)
        out_actions_w = QWidget()
        out_actions_w.setLayout(self._out_actions)
        out_header.addWidget(out_actions_w)
        out_lay.addLayout(out_header)

        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(self.DEFAULT_OUTPUT_PLACEHOLDER)
        out_lay.addWidget(self.output_text, 1)

        out_hint = QLabel("Results update after running the tool")
        out_hint.setObjectName("ioHint")
        out_lay.addWidget(out_hint)

        self._out_count_lbl = out_meta
        self._out_hint_lbl = out_hint

        out_container = QWidget()
        out_container_lay = QVBoxLayout(out_container)
        out_container_lay.setContentsMargins(0, 0, 0, 0)
        out_container_lay.addWidget(out_card)
        row.addWidget(out_container, 1)

        # Return a widget that contains the row
        wrap = QWidget()
        wrap_layout = QVBoxLayout(wrap)
        wrap_layout.setContentsMargins(0, 0, 0, 0)
        wrap_layout.addLayout(row)
        return wrap

    def _build_action_bar(self) -> QHBoxLayout:
        bar = QHBoxLayout()
        bar.setContentsMargins(0, 4, 0, 0)
        bar.setSpacing(8)
        bar.addStretch()

        self.btn_copy = QPushButton("📄  Copy Result")
        self.btn_copy.setObjectName("btnSecondary")
        self.btn_copy.clicked.connect(self._copy_result)
        bar.addWidget(self.btn_copy)

        self.btn_clear = QPushButton("🗑  Clear All")
        self.btn_clear.setObjectName("btnDangerGhost")
        self.btn_clear.clicked.connect(self._clear_all)
        bar.addWidget(self.btn_clear)

        return bar

    # ─────────────────────────────────────────── overridable hooks
    def build_controls(self, layout: QVBoxLayout):
        """Override in subclasses to add tool-specific controls."""
        pass

    # ─────────────────────────────────────────── helpers for subclasses
    def set_breadcrumb(self, text: str):
        self._breadcrumb_lbl.setText(text)
        self._breadcrumb_lbl.setVisible(bool(text))

    def set_subtitle(self, text: str):
        self._subtitle_lbl.setText(text)
        self._subtitle_lbl.setVisible(bool(text))

    def add_page_action(self, button: QPushButton):
        self._page_actions.layout().addWidget(button)

    def add_io_action(self, side: str, button: QPushButton):
        """Add a small icon button to the input or output header."""
        if side == "input":
            self._in_actions.addWidget(button)
        elif side == "output":
            self._out_actions.addWidget(button)
        else:
            raise ValueError("side must be 'input' or 'output'")

    def set_input_count(self, text: str):
        self._in_count_lbl.setText(text)

    def set_output_count(self, text: str):
        self._out_count_lbl.setText(text)

    # ───────────────────────────────────────────────────── data flow
    def set_output(self, text: str):
        """Set the output text and update global last result."""
        self.output_text.setPlainText(text)
        self._state.last_result = text

    def get_input(self) -> str:
        return self.input_text.toPlainText()

    def _copy_result(self):
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(self.output_text.toPlainText())

    def _clear_all(self):
        self.input_text.clear()
        self.output_text.clear()

    # ──────────────────────────────────────────── persistence
    def save_settings(self):
        prefix = f"Tools/{self._title}/"
        for child in self.findChildren((QLineEdit, QCheckBox, QSpinBox, QComboBox)):
            name = child.objectName()
            if not name:
                continue
            if isinstance(child, QCheckBox):
                self.settings.setValue(prefix + name, child.isChecked())
            elif isinstance(child, QLineEdit):
                self.settings.setValue(prefix + name, child.text())
            elif isinstance(child, QSpinBox):
                self.settings.setValue(prefix + name, child.value())
            elif isinstance(child, QComboBox):
                self.settings.setValue(prefix + name, child.currentText())

    def load_settings(self):
        prefix = f"Tools/{self._title}/"
        for child in self.findChildren((QLineEdit, QCheckBox, QSpinBox, QComboBox)):
            name = child.objectName()
            if not name:
                continue
            val = self.settings.value(prefix + name)
            if val is None:
                continue

            if isinstance(child, QCheckBox):
                child.setChecked(str(val).lower() == "true")
            elif isinstance(child, QLineEdit):
                child.setText(str(val))
            elif isinstance(child, QSpinBox):
                try:
                    child.setValue(int(val))
                except Exception:
                    pass
            elif isinstance(child, QComboBox):
                child.setCurrentText(str(val))
