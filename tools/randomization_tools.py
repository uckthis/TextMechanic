"""
Category 5: Randomization Tools (FULLY IMPLEMENTED)
Tools: Random Line Picker, Random Number Generator,
       Random String Generator, String Randomizer.
"""

import random
import string

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QRadioButton, QSpinBox, QButtonGroup,
    QGroupBox
)
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. Random Line Picker
# ═══════════════════════════════════════════════════════════════════════
class RandomLinePickerTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Random Line Picker", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.count_spin = QSpinBox()
        self.count_spin.setObjectName("count_spin")
        self.count_spin.setRange(1, 100000)
        self.count_spin.setValue(1)
        form.addRow("Number of lines to pick:", self.count_spin)
        layout.addLayout(form)

        self.unique_cb = QCheckBox("Pick unique lines (no repeats)")
        self.unique_cb.setObjectName("unique_cb")
        self.unique_cb.setChecked(True)
        layout.addWidget(self.unique_cb)

        btn = QPushButton("▶ Pick Random Lines")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        lines = [l for l in self.get_input().split("\n") if l.strip()]
        count = self.count_spin.value()
        if not lines:
            self.set_output("No lines to pick from.")
            return
        if self.unique_cb.isChecked():
            count = min(count, len(lines))
            picked = random.sample(lines, count)
        else:
            picked = [random.choice(lines) for _ in range(count)]
        self.set_output("\n".join(picked))


# ═══════════════════════════════════════════════════════════════════════
# 2. Random Number Generator
# ═══════════════════════════════════════════════════════════════════════
class RandomNumberGeneratorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Random Number Generator", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        form = QFormLayout()
        self.min_spin = QSpinBox()
        self.min_spin.setRange(-999999999, 999999999)
        self.min_spin.setValue(1)
        self.max_spin = QSpinBox()
        self.max_spin.setRange(-999999999, 999999999)
        self.max_spin.setValue(100)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100000)
        self.count_spin.setValue(10)
        form.addRow("Min:", self.min_spin)
        form.addRow("Max:", self.max_spin)
        form.addRow("Count:", self.count_spin)
        layout.addLayout(form)

        self.unique_cb = QCheckBox("Generate Unique Numbers")
        self.unique_cb.setObjectName("unique_cb")
        self.sort_cb = QCheckBox("Sort Results")
        self.sort_cb.setObjectName("sort_cb")
        layout.addWidget(self.unique_cb)
        layout.addWidget(self.sort_cb)

        btn = QPushButton("▶ Generate")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        lo = self.min_spin.value()
        hi = self.max_spin.value()
        count = self.count_spin.value()
        if lo > hi:
            lo, hi = hi, lo

        if self.unique_cb.isChecked():
            pool = hi - lo + 1
            if count > pool:
                self.set_output(
                    f"Cannot pick {count} unique numbers from range "
                    f"{lo}–{hi} (only {pool} possible)."
                )
                return
            nums = random.sample(range(lo, hi + 1), count)
        else:
            nums = [random.randint(lo, hi) for _ in range(count)]

        if self.sort_cb.isChecked():
            nums.sort()

        self.set_output("\n".join(str(n) for n in nums))


# ═══════════════════════════════════════════════════════════════════════
# 3. Random String Generator
# ═══════════════════════════════════════════════════════════════════════
class RandomStringGeneratorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Random String Generator", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        form = QFormLayout()
        self.length_spin = QSpinBox()
        self.length_spin.setRange(1, 10000)
        self.length_spin.setValue(16)
        self.num_strings_spin = QSpinBox()
        self.num_strings_spin.setRange(1, 10000)
        self.num_strings_spin.setValue(1)
        self.exclude_edit = QLineEdit()
        self.exclude_edit.setObjectName("exclude_edit")
        self.exclude_edit.setPlaceholderText("Characters to exclude")
        form.addRow("String Length:", self.length_spin)
        form.addRow("Number of Strings:", self.num_strings_spin)
        form.addRow("Exclude Characters:", self.exclude_edit)
        layout.addLayout(form)

        # Character sets
        grp = QGroupBox("Character Sets")
        gl = QHBoxLayout(grp)
        self.cb_upper = QCheckBox("Uppercase")
        self.cb_lower = QCheckBox("Lowercase")
        self.cb_nums = QCheckBox("Numbers")
        self.cb_syms = QCheckBox("Symbols")
        self.cb_upper.setChecked(True)
        self.cb_lower.setChecked(True)
        self.cb_nums.setChecked(True)
        gl.addWidget(self.cb_upper)
        gl.addWidget(self.cb_lower)
        gl.addWidget(self.cb_nums)
        gl.addWidget(self.cb_syms)
        layout.addWidget(grp)

        # Presets
        grp2 = QGroupBox("Presets")
        gl2 = QHBoxLayout(grp2)
        self._preset_group = QButtonGroup()
        presets = [
            ("Custom", None),
            ("Alphanumeric", (True, True, True, False)),
            ("Alpha", (True, True, False, False)),
            ("Hexadecimal", None),  # special
            ("Numeric PIN", (False, False, True, False)),
        ]
        self._preset_radios = {}
        for name, _ in presets:
            r = QRadioButton(name)
            self._preset_group.addButton(r)
            gl2.addWidget(r)
            self._preset_radios[name] = r
        self._preset_radios["Custom"].setChecked(True)
        self._preset_group.buttonClicked.connect(self._on_preset)
        layout.addWidget(grp2)

        btn = QPushButton("▶ Generate")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _on_preset(self, btn):
        name = btn.text()
        if name == "Alphanumeric":
            self.cb_upper.setChecked(True)
            self.cb_lower.setChecked(True)
            self.cb_nums.setChecked(True)
            self.cb_syms.setChecked(False)
        elif name == "Alpha":
            self.cb_upper.setChecked(True)
            self.cb_lower.setChecked(True)
            self.cb_nums.setChecked(False)
            self.cb_syms.setChecked(False)
        elif name == "Hexadecimal":
            self.cb_upper.setChecked(True)
            self.cb_lower.setChecked(False)
            self.cb_nums.setChecked(True)
            self.cb_syms.setChecked(False)
        elif name == "Numeric PIN":
            self.cb_upper.setChecked(False)
            self.cb_lower.setChecked(False)
            self.cb_nums.setChecked(True)
            self.cb_syms.setChecked(False)

    def _execute(self):
        preset = self._preset_group.checkedButton().text()
        exclude = set(self.exclude_edit.text())
        length = self.length_spin.value()
        count = self.num_strings_spin.value()

        if preset == "Hexadecimal":
            charset = "0123456789ABCDEF"
        else:
            charset = ""
            if self.cb_upper.isChecked():
                charset += string.ascii_uppercase
            if self.cb_lower.isChecked():
                charset += string.ascii_lowercase
            if self.cb_nums.isChecked():
                charset += string.digits
            if self.cb_syms.isChecked():
                charset += string.punctuation

        charset = "".join(c for c in charset if c not in exclude)
        if not charset:
            self.set_output("Error: No characters available for generation.")
            return

        results = ["".join(random.choices(charset, k=length)) for _ in range(count)]
        self.set_output("\n".join(results))


# ═══════════════════════════════════════════════════════════════════════
# 4. String Randomizer
# ═══════════════════════════════════════════════════════════════════════
class StringRandomizerTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("String Randomizer", parent)

    def build_controls(self, layout):
        btn = QPushButton("▶ Shuffle Characters")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        text = self.get_input()
        chars = list(text)
        random.shuffle(chars)
        self.set_output("".join(chars))
