"""
Category 8: All-in-One — Text Manipulation Notepad (REDESIGNED)

A master editor where operations can be queued into a pipeline and run
sequentially. Layout:

  Page header (title · subtitle · actions)
  ┌─ Operations card (left) ─┐  ┌─ Editor card (right) ─┐
  │ Operation selector       │  │ header + actions       │
  │ Operation params         │  │ notepad (Droppable)    │
  │ [Add to pipeline]        │  │ line/char count        │
  │ ── Pipeline ──           │  │                        │
  │ step list with remove    │  │                        │
  │ [Run pipeline]           │  │                        │
  └──────────────────────────┘  └────────────────────────┘
"""

import re
import unicodedata
import string as string_mod
from collections import Counter

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QPlainTextEdit, QSpinBox,
    QWidget, QStackedWidget, QApplication, QFileDialog, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QSettings
from global_state import GlobalState
from base_tool import DroppableTextEdit


class TextManipulationNotepadTool(QWidget):
    """Master notepad with a queued-operation pipeline."""

    OPERATIONS = [
        "— Select Operation —",
        "Upper Case",
        "Lower Case",
        "Title Case",
        "Sentence Case",
        "Swap Case",
        "Add Prefix/Suffix",
        "Remove Duplicate Lines",
        "Remove Empty Lines",
        "Remove Extra Spaces",
        "Remove Punctuation",
        "Remove Letter Accents",
        "Sort Lines (A→Z)",
        "Sort Lines (Z→A)",
        "Reverse Line Order",
        "Reverse Entire Text",
        "Find and Replace",
        "Add Repeats",
        "Number Each Line",
        "Word Frequency",
        "ROT13",
        "Remove Line Numbers",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = GlobalState()
        self.settings = QSettings("Antigravity", "TextManipulationTools")
        self._pipeline: list[str] = []
        self._build_ui()
        self.load_settings()

    # ───────────────────────────────────────────────────── UI assembly
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 32, 36, 32)
        root.setSpacing(20)

        # Create the notepad widget up front (referenced by editor panel)
        self.notepad = DroppableTextEdit()
        self.notepad.setPlaceholderText(
            "Type or paste text here, or drag & drop a .txt file. "
            "Build a pipeline of operations and click Run."
        )
        self.notepad.textChanged.connect(self._sync_notepad)

        # ── Page header ──────────────────────────────────────
        header = QWidget()
        header.setObjectName("pageHeader")
        hlay = QVBoxLayout(header)
        hlay.setContentsMargins(0, 0, 0, 0)
        hlay.setSpacing(4)

        # Breadcrumb
        bc = QLabel("All-in-One  /  Text Manipulation Notepad")
        bc.setObjectName("breadcrumb")
        hlay.addWidget(bc)

        # Title row
        title_row = QHBoxLayout()
        title_row.setSpacing(12)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title = QLabel("Text Manipulation Notepad")
        title.setObjectName("pageTitle")
        sub = QLabel("Edit your text in place — build a pipeline of operations and run them in sequence.")
        sub.setObjectName("pageSubtitle")
        sub.setWordWrap(True)
        title_col.addWidget(title)
        title_col.addWidget(sub)
        title_row.addLayout(title_col, 1)

        # Page actions (right side)
        self._page_actions = QWidget()
        self._page_actions.setObjectName("pageActions")
        pa = QHBoxLayout(self._page_actions)
        pa.setContentsMargins(0, 0, 0, 0)
        pa.setSpacing(8)

        self.btn_import = QPushButton("📂  Import File")
        self.btn_import.setObjectName("btnSecondary")
        self.btn_import.clicked.connect(self._open_file)
        pa.addWidget(self.btn_import)

        self.btn_save = QPushButton("💾  Save")
        self.btn_save.setObjectName("btnPrimary")
        self.btn_save.clicked.connect(self._save_file)
        pa.addWidget(self.btn_save)

        title_row.addWidget(self._page_actions, alignment=Qt.AlignmentFlag.AlignTop)
        hlay.addLayout(title_row)

        root.addWidget(header)

        # ── Body: operations panel + editor ──────────────────
        body = QHBoxLayout()
        body.setSpacing(16)
        body.addWidget(self._build_operations_panel(), 0)
        body.addWidget(self._build_editor_panel(), 1)
        root.addLayout(body, 1)

        # ── Status / info bar ────────────────────────────────
        info_row = QHBoxLayout()
        info_row.setSpacing(12)
        self.info_label = QLabel("Ready")
        self.info_label.setObjectName("fieldHint")
        info_row.addWidget(self.info_label)
        info_row.addStretch()
        self._stats_label = QLabel("0 lines · 0 characters")
        self._stats_label.setObjectName("fieldHint")
        info_row.addWidget(self._stats_label)
        root.addLayout(info_row)

    def _build_operations_panel(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(300)
        v = QVBoxLayout(card)
        v.setContentsMargins(18, 16, 18, 16)
        v.setSpacing(12)

        # Section title
        title = QLabel("OPERATIONS")
        title.setObjectName("sectionTitle")
        v.addWidget(title)

        # Operation selector
        self.op_combo = QComboBox()
        self.op_combo.setObjectName("op_combo")
        self.op_combo.addItems(self.OPERATIONS)
        self.op_combo.currentIndexChanged.connect(self._on_op_changed)
        v.addWidget(self.op_combo)

        # Dynamic params area
        self.params_stack = QStackedWidget()
        self._build_param_pages()
        v.addWidget(self.params_stack)

        # Add to pipeline button
        self.btn_add = QPushButton("＋  Add to pipeline")
        self.btn_add.setObjectName("btnSecondary")
        self.btn_add.clicked.connect(self._add_to_pipeline)
        v.addWidget(self.btn_add)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("background-color: palette(midlight); color: palette(midlight);")
        div.setFixedHeight(1)
        v.addWidget(div)

        # Pipeline section
        pipeline_title_row = QHBoxLayout()
        pipeline_title = QLabel("PIPELINE")
        pipeline_title.setObjectName("sectionTitle")
        pipeline_title_row.addWidget(pipeline_title)
        pipeline_title_row.addStretch()
        self._pipeline_count_lbl = QLabel("0 steps")
        self._pipeline_count_lbl.setObjectName("ioCount")
        pipeline_title_row.addWidget(self._pipeline_count_lbl)
        v.addLayout(pipeline_title_row)

        # Pipeline list (rebuilt dynamically)
        self._pipeline_list_widget = QWidget()
        self._pipeline_list_layout = QVBoxLayout(self._pipeline_list_widget)
        self._pipeline_list_layout.setContentsMargins(0, 0, 0, 0)
        self._pipeline_list_layout.setSpacing(4)
        self._pipeline_list_layout.addStretch(1)
        v.addWidget(self._pipeline_list_widget, 1)

        # Clear pipeline
        self.btn_clear_pipeline = QPushButton("Clear pipeline")
        self.btn_clear_pipeline.setObjectName("btnGhost")
        self.btn_clear_pipeline.clicked.connect(self._clear_pipeline)
        v.addWidget(self.btn_clear_pipeline)

        # Run pipeline (primary action)
        self.btn_run = QPushButton("▶  Run pipeline")
        self.btn_run.setObjectName("btnPrimary")
        self.btn_run.clicked.connect(self._run_pipeline)
        self.btn_run.setMinimumHeight(40)
        v.addWidget(self.btn_run)

        return card

    def _build_editor_panel(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setContentsMargins(18, 14, 18, 16)
        v.setSpacing(10)

        # Header
        header = QHBoxLayout()
        header.setSpacing(8)
        ed_title = QLabel("Editor")
        ed_title.setObjectName("ioHeader")
        header.addWidget(ed_title)
        header.addStretch()

        # IO actions
        actions = QHBoxLayout()
        actions.setSpacing(2)
        self.btn_copy = QPushButton("📄  Copy")
        self.btn_copy.setObjectName("ioIconBtn")
        self.btn_copy.setToolTip("Copy notepad content")
        self.btn_copy.clicked.connect(self._copy)
        actions.addWidget(self.btn_copy)

        self.btn_clear_np = QPushButton("🗑")
        self.btn_clear_np.setObjectName("ioIconBtn")
        self.btn_clear_np.setToolTip("Clear notepad")
        self.btn_clear_np.clicked.connect(self.notepad.clear)
        actions.addWidget(self.btn_clear_np)

        actions_w = QWidget()
        actions_w.setLayout(actions)
        header.addWidget(actions_w)
        v.addLayout(header)

        # Editor (self.notepad was created in _build_ui before this panel)
        v.addWidget(self.notepad, 1)

        # Hint
        hint = QLabel("⤵  Drag & drop a .txt, .csv, .json, .md, or .log file")
        hint.setObjectName("ioHint")
        v.addWidget(hint)

        return card

    def _build_param_pages(self):
        # Page 0: empty placeholder
        self.params_stack.addWidget(QWidget())

        # Page 1: Prefix/Suffix
        p1 = QWidget()
        f1 = QFormLayout(p1)
        f1.setContentsMargins(0, 4, 0, 0)
        f1.setVerticalSpacing(6)
        self._ps_prefix = QLineEdit()
        self._ps_prefix.setObjectName("ps_prefix")
        self._ps_prefix.setPlaceholderText("Text to add before each line")
        self._ps_suffix = QLineEdit()
        self._ps_suffix.setObjectName("ps_suffix")
        self._ps_suffix.setPlaceholderText("Text to add after each line")
        f1.addRow("Prefix:", self._ps_prefix)
        f1.addRow("Suffix:", self._ps_suffix)
        self.params_stack.addWidget(p1)

        # Page 2: Find and Replace
        p2 = QWidget()
        f2 = QFormLayout(p2)
        f2.setContentsMargins(0, 4, 0, 0)
        f2.setVerticalSpacing(6)
        self._fr_find = QLineEdit()
        self._fr_find.setObjectName("fr_find")
        self._fr_find.setPlaceholderText("Text to search for")
        self._fr_replace = QLineEdit()
        self._fr_replace.setObjectName("fr_replace")
        self._fr_replace.setPlaceholderText("Replacement text")
        f2.addRow("Find:", self._fr_find)
        f2.addRow("Replace:", self._fr_replace)
        self.params_stack.addWidget(p2)

        # Page 3: Add Repeats
        p3 = QWidget()
        f3 = QFormLayout(p3)
        f3.setContentsMargins(0, 4, 0, 0)
        f3.setVerticalSpacing(6)
        self._rep_count = QSpinBox()
        self._rep_count.setObjectName("rep_count")
        self._rep_count.setRange(1, 100000)
        self._rep_count.setValue(2)
        self._rep_sep = QLineEdit(r"\n")
        self._rep_sep.setObjectName("rep_sep")
        self._rep_sep.setPlaceholderText("\\n for newline, \\t for tab")
        f3.addRow("Times:", self._rep_count)
        f3.addRow("Separator:", self._rep_sep)
        self.params_stack.addWidget(p3)

        # Page 4: Number Each Line
        p4 = QWidget()
        f4 = QFormLayout(p4)
        f4.setContentsMargins(0, 4, 0, 0)
        f4.setVerticalSpacing(6)
        self._nel_format = QLineEdit("{n}. ")
        self._nel_format.setObjectName("nel_format")
        self._nel_format.setPlaceholderText("{n} is the line number")
        f4.addRow("Format:", self._nel_format)
        self.params_stack.addWidget(p4)

    _OP_PARAM_MAP = {
        6: 1,   # Add Prefix/Suffix
        16: 2,  # Find and Replace
        17: 3,  # Add Repeats
        18: 4,  # Number Each Line
    }

    def _on_op_changed(self, idx):
        page = self._OP_PARAM_MAP.get(idx, 0)
        self.params_stack.setCurrentIndex(page)

    # ───────────────────────────────────────────────── pipeline UI
    def _add_to_pipeline(self):
        idx = self.op_combo.currentIndex()
        if idx == 0:
            return
        op = self.OPERATIONS[idx]
        self._pipeline.append(op)
        self._render_pipeline()

    def _clear_pipeline(self):
        self._pipeline.clear()
        self._render_pipeline()

    def _render_pipeline(self):
        # Clear current list
        while self._pipeline_list_layout.count() > 1:  # keep the stretch
            item = self._pipeline_list_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        for i, op in enumerate(self._pipeline):
            row = QFrame()
            row.setObjectName("card")
            row.setStyleSheet("background-color: palette(base);")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 6, 6, 6)
            row_layout.setSpacing(8)

            num = QLabel(f"{i + 1}")
            num.setObjectName("ioCount")
            num.setFixedWidth(18)
            num.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.addWidget(num)

            name = QLabel(op)
            name.setObjectName("fieldLabel")
            name.setStyleSheet("color: palette(text);")
            name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row_layout.addWidget(name, 1)

            rm = QPushButton("×")
            rm.setObjectName("ioIconBtn")
            rm.setToolTip(f"Remove step {i + 1}")
            rm.setFixedSize(24, 24)
            rm.clicked.connect(lambda _checked, ix=i: self._remove_pipeline_step(ix))
            row_layout.addWidget(rm)

            self._pipeline_list_layout.insertWidget(self._pipeline_list_layout.count() - 1, row)

        n = len(self._pipeline)
        self._pipeline_count_lbl.setText(f"{n} step{'s' if n != 1 else ''}")

    def _remove_pipeline_step(self, index: int):
        if 0 <= index < len(self._pipeline):
            del self._pipeline[index]
            self._render_pipeline()

    # ──────────────────────────────────────────────── notepad sync
    def _sync_notepad(self):
        text = self.notepad.toPlainText()
        self._state.notepad_text = text
        lines = text.count("\n") + (1 if text else 0)
        chars = len(text)
        self._stats_label.setText(f"{lines} line{'s' if lines != 1 else ''} · {chars} character{'s' if chars != 1 else ''}")

    # ──────────────────────────────────────────────── run pipeline
    def _run_pipeline(self):
        if not self._pipeline:
            self.info_label.setText("⚠  Pipeline is empty. Add an operation first.")
            return
        text = self.notepad.toPlainText()
        if not text:
            self.info_label.setText("⚠  Editor is empty.")
            return
        for op in self._pipeline:
            text, info = self._apply_op(op, text)
            if info:
                # Could surface, but we just keep the last info
                self.info_label.setText(f"✓  {op}: {info}")
            else:
                self.info_label.setText(f"✓  Applied: {op}")
        self.notepad.setPlainText(text)
        self._state.last_result = text

    def _apply_op(self, op: str, text: str) -> tuple[str, str]:
        info = ""
        if op == "Upper Case":
            text = text.upper()
        elif op == "Lower Case":
            text = text.lower()
        elif op == "Title Case":
            text = text.title()
        elif op == "Sentence Case":
            text = re.sub(
                r'((?:^|[.!?]\s+)\s*)(\w)',
                lambda m: m.group(1) + m.group(2).upper(),
                text.lower()
            )
        elif op == "Swap Case":
            text = text.swapcase()
        elif op == "Add Prefix/Suffix":
            prefix = self._ps_prefix.text()
            suffix = self._ps_suffix.text()
            text = "\n".join(f"{prefix}{l}{suffix}" for l in text.split("\n"))
        elif op == "Remove Duplicate Lines":
            seen = set()
            out = []
            for l in text.split("\n"):
                if l not in seen:
                    out.append(l)
                    seen.add(l)
            text = "\n".join(out)
        elif op == "Remove Empty Lines":
            text = "\n".join(l for l in text.split("\n") if l.strip())
        elif op == "Remove Extra Spaces":
            text = "\n".join(re.sub(r' +', ' ', l).strip() for l in text.split("\n"))
        elif op == "Remove Punctuation":
            text = text.translate(str.maketrans('', '', string_mod.punctuation))
        elif op == "Remove Letter Accents":
            nfkd = unicodedata.normalize('NFKD', text)
            text = "".join(c for c in nfkd if not unicodedata.combining(c))
        elif op == "Sort Lines (A→Z)":
            text = "\n".join(sorted(text.split("\n"), key=str.lower))
        elif op == "Sort Lines (Z→A)":
            text = "\n".join(sorted(text.split("\n"), key=str.lower, reverse=True))
        elif op == "Reverse Line Order":
            text = "\n".join(reversed(text.split("\n")))
        elif op == "Reverse Entire Text":
            text = text[::-1]
        elif op == "Find and Replace":
            find = self._fr_find.text()
            repl = self._fr_replace.text()
            count = text.count(find)
            text = text.replace(find, repl)
            info = f"replaced {count} occurrence{'s' if count != 1 else ''}"
        elif op == "Add Repeats":
            n = self._rep_count.value()
            sep = self._rep_sep.text().replace(r"\n", "\n").replace(r"\t", "\t")
            text = sep.join([text] * n)
        elif op == "Number Each Line":
            fmt = self._nel_format.text()
            lines = text.split("\n")
            text = "\n".join(
                fmt.replace("{n}", str(i + 1)) + l
                for i, l in enumerate(lines)
            )
        elif op == "Word Frequency":
            words = re.findall(r'\b\w+\b', text.lower())
            counter = Counter(words)
            freq = [f"{w}\t{c}" for w, c in counter.most_common()]
            text = f"Unique words: {len(counter)}\n{'─' * 40}\n" + "\n".join(freq)
        elif op == "ROT13":
            import codecs
            text = codecs.encode(text, 'rot_13')
        elif op == "Remove Line Numbers":
            text = "\n".join(
                re.sub(r'^\s*\d+[\.\)\:\-]?\s?', '', l) for l in text.split("\n")
            )
        return text, info

    # ─────────────────────────────────────────────── file actions
    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "",
            "Text Files (*.txt *.csv *.log *.md *.json *.xml *.html *.ini "
            "*.cfg *.yaml *.yml *.tsv *.srt *.vtt *.py *.js *.css);;"
            "All Files (*)"
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    self.notepad.setPlainText(f.read())
                self.info_label.setText(f"✓  Loaded {os.path.basename(path)}")
            except Exception as e:
                self.info_label.setText(f"⚠  Error: {e}")

    def _save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Text File", "notepad.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.notepad.toPlainText())
                self.info_label.setText(f"✓  Saved as {os.path.basename(path)}")
            except Exception as e:
                self.info_label.setText(f"⚠  Error: {e}")

    def _copy(self):
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(self.notepad.toPlainText())
            self.info_label.setText("✓  Copied to clipboard")

    # ──────────────────────────────────────────── persistence
    def save_settings(self):
        prefix = "Tools/Text Manipulation Notepad/"
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
        prefix = "Tools/Text Manipulation Notepad/"
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
