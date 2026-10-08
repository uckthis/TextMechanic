"""
Category 7: Numeration Tools (FULLY IMPLEMENTED)
Tools: Generate List of Numbers, Number Each Line, Online Tally Counter.
"""

import re

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QComboBox, QWidget
)
from PyQt6.QtCore import Qt
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. Generate List of Numbers
# ═══════════════════════════════════════════════════════════════════════
class GenerateNumberListTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Generate List of Numbers", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        form = QFormLayout()
        self.start_spin = QSpinBox()
        self.start_spin.setObjectName("start_spin")
        self.start_spin.setRange(-999999999, 999999999)
        self.start_spin.setValue(1)
        self.step_spin = QSpinBox()
        self.step_spin.setObjectName("step_spin")
        self.step_spin.setRange(-999999, 999999)
        self.step_spin.setValue(1)
        self.count_spin = QSpinBox()
        self.count_spin.setObjectName("count_spin")
        self.count_spin.setRange(1, 100000)
        self.count_spin.setValue(10)
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setObjectName("prefix_edit")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setObjectName("suffix_edit")
        form.addRow("Start Number:", self.start_spin)
        form.addRow("Step Size:", self.step_spin)
        form.addRow("Count:", self.count_spin)
        form.addRow("Prefix:", self.prefix_edit)
        form.addRow("Suffix:", self.suffix_edit)
        layout.addLayout(form)

        btn = QPushButton("▶ Generate List")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        start = self.start_spin.value()
        step = self.step_spin.value()
        count = self.count_spin.value()
        prefix = self.prefix_edit.text()
        suffix = self.suffix_edit.text()

        lines = []
        val = start
        for _ in range(count):
            lines.append(f"{prefix}{val}{suffix}")
            val += step
        self.set_output("\n".join(lines))


# ═══════════════════════════════════════════════════════════════════════
# 2. Number Each Line
# ═══════════════════════════════════════════════════════════════════════
class NumberEachLineTool(BaseToolWidget):

    _ROMAN_VALS = [
        (1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'),
        (100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'),
        (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')
    ]

    def __init__(self, parent=None):
        super().__init__("Number Each Line", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.start_spin = QSpinBox()
        self.start_spin.setObjectName("start_spin")
        self.start_spin.setRange(1, 999999)
        self.start_spin.setValue(1)
        self.style_combo = QComboBox()
        self.style_combo.setObjectName("style_combo")
        self.style_combo.addItems([
            "Numbers (1, 2, 3…)",
            "Lower Alpha (a, b, c…)",
            "Upper Alpha (A, B, C…)",
            "Lower Roman (i, ii, iii…)",
            "Upper Roman (I, II, III…)"
        ])
        self.pad_spin = QSpinBox()
        self.pad_spin.setObjectName("pad_spin")
        self.pad_spin.setRange(0, 10)
        self.pad_spin.setValue(0)
        self.format_edit = QLineEdit("{n}. ")
        self.format_edit.setObjectName("format_edit")
        form.addRow("Start Number:", self.start_spin)
        form.addRow("Number Style:", self.style_combo)
        form.addRow("Pad Numbers:", self.pad_spin)
        form.addRow("Format string:", self.format_edit)
        layout.addLayout(form)

        btn = QPushButton("▶ Number Lines")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _to_roman(self, num):
        result = ""
        for val, numeral in self._ROMAN_VALS:
            while num >= val:
                result += numeral
                num -= val
        return result

    def _to_alpha(self, num):
        """Convert 1→a, 2→b, …, 26→z, 27→aa, …"""
        result = ""
        while num > 0:
            num -= 1
            result = chr(ord('a') + num % 26) + result
            num //= 26
        return result

    def _format_number(self, idx):
        style = self.style_combo.currentIndex()
        pad = self.pad_spin.value()
        if style == 0:  # Numbers
            s = str(idx)
            if pad > 0:
                s = s.zfill(pad)
            return s
        elif style == 1:  # Lower alpha
            return self._to_alpha(idx)
        elif style == 2:  # Upper alpha
            return self._to_alpha(idx).upper()
        elif style == 3:  # Lower roman
            return self._to_roman(idx)
        elif style == 4:  # Upper roman
            return self._to_roman(idx).upper()
        return str(idx)

    def _execute(self):
        lines = self.get_input().split("\n")
        start = self.start_spin.value()
        fmt = self.format_edit.text()
        result = []
        for i, line in enumerate(lines):
            n = self._format_number(start + i)
            prefix = fmt.replace("{n}", n)
            result.append(f"{prefix}{line}")
        self.set_output("\n".join(result))


# ═══════════════════════════════════════════════════════════════════════
# 3. Online Tally Counter
# ═══════════════════════════════════════════════════════════════════════
class TallyCounterTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Online Tally Counter", parent)
        self.input_text.parent().hide()
        self._count = 0

    def build_controls(self, layout):
        # Large count display
        self.count_label = QLabel("0")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setStyleSheet(
            "font-size: 72px; font-weight: bold; color: #a6e3a1; "
            "padding: 20px; border: 2px solid #313244; border-radius: 12px; "
            "background-color: #11111b; margin: 10px;"
        )
        layout.addWidget(self.count_label, 1)

        # Buttons
        row1 = QHBoxLayout()
        for text, delta in [("+1", 1), ("+5", 5), ("+10", 10)]:
            btn = QPushButton(text)
            btn.setObjectName("executeBtn")
            btn.setStyleSheet("font-size:16px; padding:12px 24px;")
            btn.clicked.connect(lambda _, d=delta: self._adjust(d))
            row1.addWidget(btn)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        for text, delta in [("-1", -1), ("-5", -5), ("-10", -10)]:
            btn = QPushButton(text)
            btn.setStyleSheet(
                "font-size:16px; padding:12px 24px; "
                "background-color:#f38ba8; color:#1e1e2e; font-weight:bold; "
                "border:none; border-radius:6px;"
            )
            btn.clicked.connect(lambda _, d=delta: self._adjust(d))
            row2.addWidget(btn)
        layout.addLayout(row2)

        reset_btn = QPushButton("Reset")
        reset_btn.setStyleSheet(
            "font-size:14px; padding:8px 20px; background-color:#fab387; "
            "color:#1e1e2e; font-weight:bold; border:none; border-radius:6px;"
        )
        reset_btn.clicked.connect(self._reset)
        layout.addWidget(reset_btn)

    def _adjust(self, delta):
        self._count += delta
        self.count_label.setText(str(self._count))
        self.set_output(str(self._count))

    def _reset(self):
        self._count = 0
        self.count_label.setText("0")
        self.set_output("0")
