"""
Category 2: Extraction & Analysis Tools
Fully implemented: Extract Text Between Strings, Word Frequency Counter.
"""

import re
from collections import Counter

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QRadioButton, QSpinBox, QButtonGroup,
    QPlainTextEdit, QGroupBox, QApplication
)
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. Extract Text Between Strings
# ═══════════════════════════════════════════════════════════════════════
class ExtractBetweenStringsTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Extract Text Between Strings", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.start_edit = QLineEdit()
        self.start_edit.setObjectName("start_edit")
        self.start_edit.setPlaceholderText("Start delimiter")
        self.end_edit = QLineEdit()
        self.end_edit.setObjectName("end_edit")
        self.end_edit.setPlaceholderText("End delimiter")
        form.addRow("Start Delimiter:", self.start_edit)
        form.addRow("End Delimiter:", self.end_edit)
        layout.addLayout(form)

        self.case_cb = QCheckBox("Case Sensitive Delimiters")
        self.case_cb.setObjectName("case_cb")
        self.case_cb.setChecked(True)
        self.include_cb = QCheckBox("Include Delimiters in Result")
        self.include_cb.setObjectName("include_cb")
        self.regex_cb = QCheckBox("Use Regex for Delimiters")
        self.regex_cb.setObjectName("regex_cb")
        layout.addWidget(self.case_cb)
        layout.addWidget(self.include_cb)
        layout.addWidget(self.regex_cb)

        btn = QPushButton("▶ Extract")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        text = self.get_input()
        start = self.start_edit.text()
        end = self.end_edit.text()
        if not start or not end:
            self.set_output("Please provide both start and end delimiters.")
            return

        case = self.case_cb.isChecked()
        include = self.include_cb.isChecked()
        use_regex = self.regex_cb.isChecked()
        flags = 0 if case else re.IGNORECASE

        if use_regex:
            s_pat = start
            e_pat = end
        else:
            s_pat = re.escape(start)
            e_pat = re.escape(end)

        if include:
            pattern = f"({s_pat}.*?{e_pat})"
        else:
            pattern = f"{s_pat}(.*?){e_pat}"

        try:
            matches = re.findall(pattern, text, flags | re.DOTALL)
        except re.error as e:
            self.set_output(f"Regex error: {e}")
            return

        if matches:
            self.set_output("\n".join(matches))
        else:
            self.set_output("No matches found.")


# ═══════════════════════════════════════════════════════════════════════
# 2. Word Frequency Counter
# ═══════════════════════════════════════════════════════════════════════
class WordFrequencyCounterTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Word Frequency Counter", parent)

    def build_controls(self, layout):
        opts = QHBoxLayout()
        self.case_cb = QCheckBox("Case Sensitive Counting")
        self.case_cb.setObjectName("case_cb")
        self.min_len_spin = QSpinBox()
        self.min_len_spin.setObjectName("min_len_spin")
        self.min_len_spin.setRange(1, 50)
        self.min_len_spin.setValue(1)
        opts.addWidget(self.case_cb)
        opts.addWidget(QLabel("Min Word Length:"))
        opts.addWidget(self.min_len_spin)
        opts.addStretch()
        layout.addLayout(opts)

        # Sort options
        grp = QGroupBox("Sort By")
        gl = QHBoxLayout(grp)
        self.sort_count_desc = QRadioButton("Count (High→Low)")
        self.sort_count_asc = QRadioButton("Count (Low→High)")
        self.sort_word_az = QRadioButton("Word (A→Z)")
        self.sort_word_za = QRadioButton("Word (Z→A)")
        self.sort_count_desc.setChecked(True)
        self._sort_grp = QButtonGroup()
        self._sort_grp.addButton(self.sort_count_desc)
        self._sort_grp.addButton(self.sort_count_asc)
        self._sort_grp.addButton(self.sort_word_az)
        self._sort_grp.addButton(self.sort_word_za)
        gl.addWidget(self.sort_count_desc)
        gl.addWidget(self.sort_count_asc)
        gl.addWidget(self.sort_word_az)
        gl.addWidget(self.sort_word_za)
        layout.addWidget(grp)

        btn_row = QHBoxLayout()
        btn_count = QPushButton("▶ Count Words")
        btn_count.setObjectName("executeBtn")
        btn_csv = QPushButton("📄 Copy as CSV")
        btn_csv.setObjectName("actionBtn")
        btn_count.clicked.connect(self._count_words)
        btn_csv.clicked.connect(self._copy_csv)
        btn_row.addWidget(btn_count)
        btn_row.addWidget(btn_csv)
        layout.addLayout(btn_row)

        self._freq_data = []

    def _count_words(self):
        text = self.get_input()
        case = self.case_cb.isChecked()
        min_len = self.min_len_spin.value()

        words = re.findall(r'\b\w+\b', text)
        if not case:
            words = [w.lower() for w in words]
        words = [w for w in words if len(w) >= min_len]

        counter = Counter(words)

        if self.sort_count_desc.isChecked():
            items = counter.most_common()
        elif self.sort_count_asc.isChecked():
            items = sorted(counter.items(), key=lambda x: x[1])
        elif self.sort_word_az.isChecked():
            items = sorted(counter.items(), key=lambda x: x[0])
        else:
            items = sorted(counter.items(), key=lambda x: x[0], reverse=True)

        self._freq_data = items
        lines = [f"{word}\t{count}" for word, count in items]
        header = f"Total unique words: {len(items)}\n{'─' * 40}\n"
        self.set_output(header + "\n".join(lines))

    def _copy_csv(self):
        if not self._freq_data:
            return
        csv_lines = ["Word,Count"] + [f"{w},{c}" for w, c in self._freq_data]
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText("\n".join(csv_lines))
