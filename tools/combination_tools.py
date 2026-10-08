"""
Category 6: Combination / Permutation (FULLY IMPLEMENTED)
Tools: Combination Generator (nCk), Lists Comparison Tool,
       Line Combination Generator (Cartesian Product), Permutation Generator (n!).
"""

import itertools

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QRadioButton, QSpinBox, QButtonGroup,
    QPlainTextEdit, QGroupBox, QWidget, QSplitter, QApplication
)
from PyQt6.QtCore import Qt
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. Combination Generator (nCk)
# ═══════════════════════════════════════════════════════════════════════
class CombinationGeneratorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Combination Generator (nCk)", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.k_spin = QSpinBox()
        self.k_spin.setObjectName("k_spin")
        self.k_spin.setRange(1, 100)
        self.k_spin.setValue(2)
        self.sep_edit = QLineEdit(", ")
        self.sep_edit.setObjectName("sep_edit")
        form.addRow("Combination Size 'k':", self.k_spin)
        form.addRow("Separator within combination:", self.sep_edit)
        layout.addLayout(form)

        btn = QPushButton("▶ Generate Combinations")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        items = [l for l in self.get_input().split("\n") if l.strip()]
        k = self.k_spin.value()
        sep = self.sep_edit.text()

        if k > len(items):
            self.set_output(f"Error: k ({k}) is larger than the number of items ({len(items)}).")
            return

        combos = list(itertools.combinations(items, k))
        if len(combos) > 50000:
            self.set_output(
                f"Warning: {len(combos)} combinations generated. "
                f"Showing first 50,000."
            )
            combos = combos[:50000]

        result = [sep.join(c) for c in combos]
        self.set_output("\n".join(result))


# ═══════════════════════════════════════════════════════════════════════
# 2. Lists Comparison Tool
# ═══════════════════════════════════════════════════════════════════════
class ListsComparisonTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Lists Comparison Tool", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        # Two input lists
        splitter = QSplitter(Qt.Orientation.Horizontal)
        w1 = QWidget()
        l1 = QVBoxLayout(w1)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(QLabel("List A"))
        self.list_a = QPlainTextEdit()
        l1.addWidget(self.list_a)
        splitter.addWidget(w1)

        w2 = QWidget()
        l2 = QVBoxLayout(w2)
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addWidget(QLabel("List B"))
        self.list_b = QPlainTextEdit()
        l2.addWidget(self.list_b)
        splitter.addWidget(w2)
        layout.addWidget(splitter)

        # Options
        opts = QHBoxLayout()
        self.case_cb = QCheckBox("Case Sensitive")
        self.case_cb.setObjectName("case_cb")
        self.case_cb.setChecked(True)
        self.trim_cb = QCheckBox("Trim whitespace")
        self.trim_cb.setObjectName("trim_cb")
        self.whole_cb = QCheckBox("Match Whole Word")
        self.whole_cb.setObjectName("whole_cb")
        opts.addWidget(self.case_cb)
        opts.addWidget(self.trim_cb)
        opts.addWidget(self.whole_cb)
        layout.addLayout(opts)

        # Output casing
        grp = QGroupBox("Output Casing")
        gl = QHBoxLayout(grp)
        self.case_a = QRadioButton("Use casing from A")
        self.case_b = QRadioButton("Use casing from B")
        self.case_lower = QRadioButton("Convert to lowercase")
        self.case_a.setChecked(True)
        self._case_grp = QButtonGroup()
        self._case_grp.addButton(self.case_a)
        self._case_grp.addButton(self.case_b)
        self._case_grp.addButton(self.case_lower)
        gl.addWidget(self.case_a)
        gl.addWidget(self.case_b)
        gl.addWidget(self.case_lower)
        layout.addWidget(grp)

        btn = QPushButton("▶ Compare Lists")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

        # Four output areas
        out_splitter = QSplitter(Qt.Orientation.Horizontal)
        self._out_areas = {}
        for name in ["A only", "B only", "Both", "All Unique"]:
            w = QWidget()
            vl = QVBoxLayout(w)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.addWidget(QLabel(name))
            area = QPlainTextEdit()
            area.setReadOnly(True)
            vl.addWidget(area)
            out_splitter.addWidget(w)
            self._out_areas[name] = area
        layout.addWidget(out_splitter, 1)

    def _execute(self):
        raw_a = self.list_a.toPlainText().split("\n")
        raw_b = self.list_b.toPlainText().split("\n")
        trim = self.trim_cb.isChecked()
        case = self.case_cb.isChecked()

        def normalize(s):
            if trim:
                s = s.strip()
            if not case:
                return s.lower()
            return s

        # Build lookup maps: normalized → original items
        map_a = {}
        for item in raw_a:
            if not item.strip():
                continue
            key = normalize(item)
            if key not in map_a:
                map_a[key] = item

        map_b = {}
        for item in raw_b:
            if not item.strip():
                continue
            key = normalize(item)
            if key not in map_b:
                map_b[key] = item

        set_a = set(map_a.keys())
        set_b = set(map_b.keys())

        a_only_keys = set_a - set_b
        b_only_keys = set_b - set_a
        both_keys = set_a & set_b
        all_unique_keys = set_a | set_b

        def pick_casing(key):
            if self.case_lower.isChecked():
                return key
            elif self.case_b.isChecked():
                return map_b.get(key, map_a.get(key, key))
            else:
                return map_a.get(key, map_b.get(key, key))

        self._out_areas["A only"].setPlainText(
            "\n".join(pick_casing(k) for k in sorted(a_only_keys)))
        self._out_areas["B only"].setPlainText(
            "\n".join(pick_casing(k) for k in sorted(b_only_keys)))
        self._out_areas["Both"].setPlainText(
            "\n".join(pick_casing(k) for k in sorted(both_keys)))
        self._out_areas["All Unique"].setPlainText(
            "\n".join(pick_casing(k) for k in sorted(all_unique_keys)))

        self.set_output(
            f"A only: {len(a_only_keys)}  |  "
            f"B only: {len(b_only_keys)}  |  "
            f"Both: {len(both_keys)}  |  "
            f"All Unique: {len(all_unique_keys)}"
        )


# ═══════════════════════════════════════════════════════════════════════
# 3. Line Combination Generator (Cartesian Product)
# ═══════════════════════════════════════════════════════════════════════
class LineCombinationGeneratorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Line Combination Generator (Cartesian Product)", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self._lists = []
        for name in ["List 1", "List 2", "List 3 (optional)"]:
            w = QWidget()
            vl = QVBoxLayout(w)
            vl.setContentsMargins(0, 0, 0, 0)
            vl.addWidget(QLabel(name))
            area = QPlainTextEdit()
            vl.addWidget(area)
            splitter.addWidget(w)
            self._lists.append(area)
        layout.addWidget(splitter, 1)

        form = QFormLayout()
        self.sep_edit = QLineEdit(" ")
        form.addRow("Separator:", self.sep_edit)
        layout.addLayout(form)

        btn = QPushButton("▶ Generate Cartesian Product")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        sep = self.sep_edit.text()
        pools = []
        for area in self._lists:
            items = [l for l in area.toPlainText().split("\n") if l.strip()]
            if items:
                pools.append(items)

        if len(pools) < 2:
            self.set_output("Please provide at least 2 non-empty lists.")
            return

        product = list(itertools.product(*pools))
        if len(product) > 100000:
            self.set_output(
                f"Warning: {len(product)} combinations. Showing first 100,000."
            )
            product = product[:100000]

        result = [sep.join(combo) for combo in product]
        self.set_output("\n".join(result))


# ═══════════════════════════════════════════════════════════════════════
# 4. Permutation Generator (n!)
# ═══════════════════════════════════════════════════════════════════════
class PermutationGeneratorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Permutation Generator (n!)", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.sep_edit = QLineEdit(", ")
        form.addRow("Separator within permutation:", self.sep_edit)
        layout.addLayout(form)

        btn = QPushButton("▶ Generate Permutations")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        items = [l for l in self.get_input().split("\n") if l.strip()]
        sep = self.sep_edit.text()

        if len(items) > 8:
            self.set_output(
                f"Warning: {len(items)}! = very large output. "
                f"Limiting to items ≤ 8. Please reduce your list."
            )
            return

        perms = list(itertools.permutations(items))
        result = [sep.join(p) for p in perms]
        self.set_output("\n".join(result))
