"""

Category 1: Basic Text Tools

All 18 tool widgets, each subclassing BaseToolWidget.

"""



import re

import unicodedata



from PyQt6.QtWidgets import (

    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,

    QPushButton, QCheckBox, QRadioButton, QSpinBox, QComboBox,

    QPlainTextEdit, QGroupBox, QButtonGroup, QWidget, QSplitter,

    QApplication, QFrame, QSizePolicy

)

from PyQt6.QtCore import Qt

from base_tool import BaseToolWidget





# ═══════════════════════════════════════════════════════════════════════

# 1. Add Prefix / Suffix / Delimiter

# ═══════════════════════════════════════════════════════════════════════

class AddPrefixSuffixTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Add Prefix / Suffix / Delimiter", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.prefix_edit = QLineEdit()

        self.prefix_edit.setObjectName("prefix_edit")

        self.suffix_edit = QLineEdit()

        self.suffix_edit.setObjectName("suffix_edit")

        self.join_edit = QLineEdit(r"\n")

        self.join_edit.setObjectName("join_edit")

        form.addRow("Prefix:", self.prefix_edit)

        form.addRow("Suffix:", self.suffix_edit)

        form.addRow("Join Lines With:", self.join_edit)

        layout.addLayout(form)



        self.skip_empty_cb = QCheckBox("Skip adding prefix/suffix to empty/whitespace lines")

        self.skip_empty_cb.setObjectName("skip_empty_cb")

        layout.addWidget(self.skip_empty_cb)



        btn = QPushButton("▶ Apply")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        text = self.get_input()

        prefix = self.prefix_edit.text()

        suffix = self.suffix_edit.text()

        join_str = self.join_edit.text().replace(r"\n", "\n").replace(r"\t", "\t")

        skip_empty = self.skip_empty_cb.isChecked()



        lines = text.split("\n")

        result = []

        for line in lines:

            if skip_empty and line.strip() == "":

                result.append(line)

            else:

                result.append(f"{prefix}{line}{suffix}")

        self.set_output(join_str.join(result))





# ═══════════════════════════════════════════════════════════════════════

# 2. Add / Remove Line Breaks

# ═══════════════════════════════════════════════════════════════════════

class AddRemoveLineBreaksTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Add / Remove Line Breaks", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.break_char_edit = QLineEdit()

        self.break_char_edit.setObjectName("break_char_edit")

        self.break_char_edit.setPlaceholderText("Character(s) to use")

        form.addRow("Break Character(s):", self.break_char_edit)

        layout.addLayout(form)



        row = QHBoxLayout()

        btn1 = QPushButton("Remove All Line Breaks")

        btn2 = QPushButton("Add Break After Sentences (.!?)")

        btn3 = QPushButton("Add Break After Character(s)")

        btn1.setObjectName("executeBtn")

        btn2.setObjectName("executeBtn")

        btn3.setObjectName("executeBtn")

        btn1.clicked.connect(self._remove_all)

        btn2.clicked.connect(self._after_sentences)

        btn3.clicked.connect(self._after_chars)

        row.addWidget(btn1)

        row.addWidget(btn2)

        row.addWidget(btn3)

        layout.addLayout(row)



    def _remove_all(self):

        self.set_output(self.get_input().replace("\n", "").replace("\r", ""))



    def _after_sentences(self):

        text = self.get_input()

        result = re.sub(r'([.!?])\s*', r'\1\n', text)

        self.set_output(result)



    def _after_chars(self):

        text = self.get_input()

        chars = self.break_char_edit.text()

        if not chars:

            return

        result = text.replace(chars, chars + "\n")

        self.set_output(result)





# ═══════════════════════════════════════════════════════════════════════

# 3. Add Repeats

# ═══════════════════════════════════════════════════════════════════════

class AddRepeatsTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Add Repeats", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.count_spin = QSpinBox()

        self.count_spin.setObjectName("count_spin")

        self.count_spin.setRange(1, 100000)

        self.count_spin.setValue(2)

        self.separator_edit = QLineEdit(r"\n")

        self.separator_edit.setObjectName("separator_edit")

        form.addRow("Number of Times:", self.count_spin)

        form.addRow("Separator:", self.separator_edit)

        layout.addLayout(form)



        btn = QPushButton("▶ Repeat Text")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        text = self.get_input()

        count = self.count_spin.value()

        sep = self.separator_edit.text().replace(r"\n", "\n").replace(r"\t", "\t")

        self.set_output(sep.join([text] * count))





# ═══════════════════════════════════════════════════════════════════════

# 4. Count Characters, Words, etc.

# ═══════════════════════════════════════════════════════════════════════

class CountCharsTool(BaseToolWidget):

    """Live text metrics — no separate output box needed."""



    def __init__(self, parent=None):

        super().__init__("Count Characters, Words, etc.", parent)

        self.input_text.textChanged.connect(self._update_counts)

        self._update_counts()



    def build_controls(self, layout):

        self._labels = {}

        grid = QFormLayout()

        for name in ["Characters", "Words", "Sentences", "Lines",

                      "Whitespace Chars", "Non-Whitespace Chars", "Bytes"]:

            lbl = QLabel("0")

            lbl.setStyleSheet("font-size:14px; font-weight:bold; color:#a6e3a1;")

            self._labels[name] = lbl

            grid.addRow(f"{name}:", lbl)

        layout.addLayout(grid)



    def _update_counts(self):

        t = self.get_input()

        self._labels["Characters"].setText(str(len(t)))

        self._labels["Words"].setText(str(len(t.split()) if t.strip() else 0))

        self._labels["Sentences"].setText(str(len(re.findall(r'[.!?]+', t)) if t.strip() else 0))

        self._labels["Lines"].setText(str(t.count("\n") + 1 if t else 0))

        self._labels["Whitespace Chars"].setText(str(sum(1 for c in t if c.isspace())))

        self._labels["Non-Whitespace Chars"].setText(str(sum(1 for c in t if not c.isspace())))

        self._labels["Bytes"].setText(str(len(t.encode('utf-8'))))





# ═══════════════════════════════════════════════════════════════════════

# 5. Delimited Column Extractor

# ═══════════════════════════════════════════════════════════════════════

class SplitTextTool(BaseToolWidget):

    """

    Split delimited text into columns.



    Default behavior: outputs ALL columns side-by-side, separated by tab —

    perfect for pasting into a spreadsheet. Optional modes let you pick

    specific columns or extract a single column.

    """



    def __init__(self, parent=None):

        super().__init__("Split Text by Delimiter", parent)

        self.set_subtitle(

            "Split text by a delimiter (comma, tab, colon, etc.) and pull out the columns you need."

        )

        # Wire input → live preview (input_text exists after super().__init__)

        self.input_text.textChanged.connect(self._update_preview)

        # Run the initial preview now that everything is built

        self._update_preview()



    # ──────────────────────────────────────────── UI

    def build_controls(self, layout):

        # ── Card 1: Parsing

        parsing_card = QFrame()

        parsing_card.setObjectName("card")

        p = QVBoxLayout(parsing_card)

        p.setContentsMargins(18, 14, 18, 16)

        p.setSpacing(12)



        title = QLabel("PARSING")

        title.setObjectName("sectionTitle")

        p.addWidget(title)



        # Delimiter row

        delim_row = QHBoxLayout()

        delim_lbl = QLabel("Delimiter")

        delim_lbl.setObjectName("fieldLabel")

        delim_lbl.setFixedWidth(140)

        self.delim_edit = QLineEdit(",")

        self.delim_edit.setObjectName("delim_edit")

        self.delim_edit.setPlaceholderText(",  |  :  ;  \\t  (use \\t for tab)")

        self.delim_edit.textChanged.connect(self._update_preview)

        delim_row.addWidget(delim_lbl)

        delim_row.addWidget(self.delim_edit, 1)

        p.addLayout(delim_row)



        # Options

        opts = QHBoxLayout()

        opts.setSpacing(20)

        self.trim_cb = QCheckBox("Trim whitespace around columns")

        self.trim_cb.setObjectName("trim_cb")

        self.trim_cb.setChecked(True)

        self.trim_cb.stateChanged.connect(self._update_preview)

        opts.addWidget(self.trim_cb)



        self.skip_empty_cb = QCheckBox("Skip empty input lines")

        self.skip_empty_cb.setObjectName("skip_empty_cb")

        self.skip_empty_cb.stateChanged.connect(self._update_preview)

        opts.addWidget(self.skip_empty_cb)

        opts.addStretch()

        p.addLayout(opts)



        layout.addWidget(parsing_card)



        # ── Card 2: Output mode

        mode_card = QFrame()

        mode_card.setObjectName("card")

        m = QVBoxLayout(mode_card)

        m.setContentsMargins(18, 14, 18, 16)

        m.setSpacing(12)



        out_title = QLabel("OUTPUT")

        out_title.setObjectName("sectionTitle")

        m.addWidget(out_title)



        # Mode radios

        radios = QHBoxLayout()

        radios.setSpacing(20)

        self.mode_all = QRadioButton("All columns side-by-side")

        self.mode_all.setObjectName("mode_all")

        self.mode_all.setChecked(True)

        self.mode_all.toggled.connect(self._on_mode_changed)



        self.mode_selected = QRadioButton("Selected columns only")

        self.mode_selected.setObjectName("mode_selected")

        self.mode_selected.toggled.connect(self._on_mode_changed)



        self.mode_one = QRadioButton("One column per line, by index")

        self.mode_one.setObjectName("mode_one")

        self.mode_one.toggled.connect(self._on_mode_changed)



        radios.addWidget(self.mode_all)

        radios.addWidget(self.mode_selected)

        radios.addWidget(self.mode_one)

        radios.addStretch()

        m.addLayout(radios)



        # Selected columns input

        sel_row = QHBoxLayout()

        sel_lbl = QLabel("Column numbers")

        sel_lbl.setObjectName("fieldLabel")

        sel_lbl.setFixedWidth(140)

        self.cols_edit = QLineEdit("1")

        self.cols_edit.setObjectName("cols_edit")

        self.cols_edit.setPlaceholderText("e.g. 1, 3, 5  (1-based)")

        self.cols_edit.setEnabled(False)

        self.cols_edit.textChanged.connect(self._update_preview)

        sel_row.addWidget(sel_lbl)

        sel_row.addWidget(self.cols_edit, 1)

        m.addLayout(sel_row)



        # One column index

        one_row = QHBoxLayout()

        one_lbl = QLabel("Column number")

        one_lbl.setObjectName("fieldLabel")

        one_lbl.setFixedWidth(140)

        self.one_col_edit = QSpinBox()

        self.one_col_edit.setObjectName("one_col_edit")

        self.one_col_edit.setRange(1, 99)

        self.one_col_edit.setValue(1)

        self.one_col_edit.setEnabled(False)

        self.one_col_edit.valueChanged.connect(self._update_preview)

        one_row.addWidget(one_lbl)

        one_row.addWidget(self.one_col_edit, 1)

        one_row.addStretch()

        m.addLayout(one_row)



        # Output separator

        sep_row = QHBoxLayout()

        sep_lbl = QLabel("Output separator")

        sep_lbl.setObjectName("fieldLabel")

        sep_lbl.setFixedWidth(140)

        self.sep_edit = QLineEdit(r"\t")

        self.sep_edit.setObjectName("sep_edit")

        self.sep_edit.setPlaceholderText("\\t for tab, , for comma, etc.")

        sep_row.addWidget(sep_lbl)

        sep_row.addWidget(self.sep_edit, 1)

        m.addLayout(sep_row)



        layout.addWidget(mode_card)



        # ── Card 3: Live preview

        preview_card = QFrame()

        preview_card.setObjectName("card")

        pv = QVBoxLayout(preview_card)

        pv.setContentsMargins(18, 14, 18, 16)

        pv.setSpacing(10)



        pv_title = QLabel("PREVIEW (first row split into columns)")

        pv_title.setObjectName("sectionTitle")

        pv.addWidget(pv_title)



        self.preview_lbl = QLabel()

        self.preview_lbl.setObjectName("fieldHint")

        self.preview_lbl.setWordWrap(True)

        self.preview_lbl.setTextFormat(Qt.TextFormat.RichText)

        pv.addWidget(self.preview_lbl)



        layout.addWidget(preview_card)



        # Primary action — matches other process buttons (#executeBtn)

        self._extract_btn = QPushButton("▶  Extract Columns")

        self._extract_btn.setObjectName("executeBtn")

        self._extract_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._extract_btn.clicked.connect(self._execute)

        layout.addWidget(self._extract_btn)



    # ──────────────────────────────────────────── helpers

    def _interpret_escape(self, text: str) -> str:

        """Allow \\t, \\n in the delimiter/separator strings."""

        if not text:

            return ""

        if text == r"\t":

            return "\t"

        if text == r"\n":

            return "\n"

        return text



    def _split_first_row(self) -> list[str]:

        delim = self._interpret_escape(self.delim_edit.text() or ",")

        text = self.get_input()

        if not text:

            return []

        first = text.split("\n", 1)[0]

        parts = first.split(delim)

        if self.trim_cb.isChecked():

            parts = [p.strip() for p in parts]

        return parts



    def _update_preview(self):

        parts = self._split_first_row()

        if not parts:

            self.preview_lbl.setText(

                '<span style="color: #A8A29E;">Type or paste text in the input to see how it splits.</span>'

            )

            return

        n = len(parts)

        # Display each column as a colored chip

        chips = []

        for i, p in enumerate(parts):

            display = p if p else "(empty)"

            chips.append(

                f'<span style="background-color: rgba(217,119,6,0.14); '

                f'color: #92400E; padding: 3px 8px; border-radius: 6px; '

                f'margin-right: 4px; font-family: JetBrains Mono, Consolas, monospace;">'

                f'{i + 1}: {display}</span>'

            )

        self.preview_lbl.setText(

            f'<span style="color: #57534E; font-weight: 600;">{n} column{"s" if n != 1 else ""}:</span> '

            + " ".join(chips)

        )



    def _on_mode_changed(self):

        self.cols_edit.setEnabled(self.mode_selected.isChecked())

        self.one_col_edit.setEnabled(self.mode_one.isChecked())

        self._update_preview()



    # ──────────────────────────────────────────── execute

    def _execute(self):

        text = self.get_input()

        if not text.strip():

            self.set_output("")

            self.set_output_count("No input")

            return



        delim = self._interpret_escape(self.delim_edit.text() or ",")

        join_str = self._interpret_escape(self.sep_edit.text() or "\t")

        if join_str == "":

            join_str = "\t"

        trim = self.trim_cb.isChecked()

        skip_empty = self.skip_empty_cb.isChecked()



        lines = text.split("\n")

        if skip_empty:

            lines = [l for l in lines if l.strip()]



        rows = []

        for line in lines:

            parts = line.split(delim)

            if trim:

                parts = [p.strip() for p in parts]

            rows.append(parts)



        if not rows:

            self.set_output("")

            self.set_output_count("No rows after filtering")

            return



        if self.mode_all.isChecked():

            result_lines = [join_str.join(parts) for parts in rows]

        elif self.mode_selected.isChecked():

            try:

                col_indices = [

                    int(c.strip()) - 1

                    for c in self.cols_edit.text().split(",")

                    if c.strip()

                ]

            except ValueError:

                self.set_output("Error: column numbers must be integers (1-based).")

                self.set_output_count("Error")

                return

            result_lines = [

                join_str.join(parts[i] for i in col_indices if 0 <= i < len(parts))

                for parts in rows

            ]

        elif self.mode_one.isChecked():

            col_idx = self.one_col_edit.value() - 1

            result_lines = [

                (parts[col_idx] if 0 <= col_idx < len(parts) else "")

                for parts in rows

            ]

        else:

            result_lines = []



        result = "\n".join(result_lines)

        self.set_output(result)

        self.set_output_count(

            f"{len(result_lines)} line{'s' if len(result_lines) != 1 else ''} · "

            f"{len(result)} char{'s' if len(result) != 1 else ''}"

        )





# ═══════════════════════════════════════════════════════════════════════

# 6. Find and Replace Text

# ═══════════════════════════════════════════════════════════════════════

class FindReplaceTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Find and Replace Text", parent)



    def build_controls(self, layout):

        # Options

        opts = QHBoxLayout()

        self.case_cb = QCheckBox("Case Sensitive")

        self.case_cb.setObjectName("case_cb")

        self.regex_cb = QCheckBox("Use Regular Expression")

        self.regex_cb.setObjectName("regex_cb")

        self.multiline_cb = QCheckBox("Multiline Mode")

        self.multiline_cb.setObjectName("multiline_cb")

        opts.addWidget(self.case_cb)

        opts.addWidget(self.regex_cb)

        opts.addWidget(self.multiline_cb)

        layout.addLayout(opts)



        # Mode toggle

        mode_row = QHBoxLayout()

        self.single_radio = QRadioButton("Single Find/Replace")

        self.multi_radio = QRadioButton("Multiple Find/Replace Pairs")

        self.single_radio.setChecked(True)

        self._mode_group = QButtonGroup()

        self._mode_group.addButton(self.single_radio)

        self._mode_group.addButton(self.multi_radio)

        mode_row.addWidget(self.single_radio)

        mode_row.addWidget(self.multi_radio)

        layout.addLayout(mode_row)



        # Single mode

        self.single_widget = QWidget()

        sf = QFormLayout(self.single_widget)

        sf.setContentsMargins(0, 0, 0, 0)

        self.find_edit = QLineEdit()

        self.find_edit.setObjectName("find_edit")

        self.replace_edit = QLineEdit()

        self.replace_edit.setObjectName("replace_edit")

        sf.addRow("Find:", self.find_edit)

        sf.addRow("Replace With:", self.replace_edit)

        layout.addWidget(self.single_widget)



        # Multi mode

        self.multi_widget = QWidget()

        mf = QHBoxLayout(self.multi_widget)

        mf.setContentsMargins(0, 0, 0, 0)

        left = QVBoxLayout()

        left.addWidget(QLabel("Find List (one per line)"))

        self.find_list = QPlainTextEdit()

        self.find_list.setObjectName("find_list")

        self.find_list.setMaximumHeight(100)

        left.addWidget(self.find_list)

        right = QVBoxLayout()

        right.addWidget(QLabel("Replace List (one per line)"))

        self.replace_list = QPlainTextEdit()

        self.replace_list.setObjectName("replace_list")

        self.replace_list.setMaximumHeight(100)

        right.addWidget(self.replace_list)

        mf.addLayout(left)

        mf.addLayout(right)

        self.multi_widget.hide()

        layout.addWidget(self.multi_widget)



        # Toggle visibility

        self.single_radio.toggled.connect(lambda c: (self.single_widget.setVisible(c),

                                                      self.multi_widget.setVisible(not c)))



        # Buttons

        btn_row = QHBoxLayout()

        btn_replace = QPushButton("▶ Replace All")

        btn_replace.setObjectName("executeBtn")

        btn_count = QPushButton("Count Matches")

        btn_replace.clicked.connect(self._replace_all)

        btn_count.clicked.connect(self._count_matches)

        btn_row.addWidget(btn_replace)

        btn_row.addWidget(btn_count)

        layout.addLayout(btn_row)



    def _get_flags(self):

        flags = 0

        if not self.case_cb.isChecked():

            flags |= re.IGNORECASE

        if self.multiline_cb.isChecked():

            flags |= re.MULTILINE

        return flags



    def _replace_all(self):

        text = self.get_input()

        use_regex = self.regex_cb.isChecked()

        flags = self._get_flags()



        if self.single_radio.isChecked():

            find = self.find_edit.text()

            repl = self.replace_edit.text()

            if use_regex:

                try:

                    text = re.sub(find, repl, text, flags=flags)

                except re.error as e:

                    self.set_output(f"Regex error: {e}")

                    return

            else:

                if self.case_cb.isChecked():

                    text = text.replace(find, repl)

                else:

                    text = re.sub(re.escape(find), repl, text, flags=flags)

        else:

            finds = self.find_list.toPlainText().split("\n")

            repls = self.replace_list.toPlainText().split("\n")

            for i, f in enumerate(finds):

                r = repls[i] if i < len(repls) else ""

                if not f:

                    continue

                if use_regex:

                    try:

                        text = re.sub(f, r, text, flags=flags)

                    except re.error as e:

                        self.set_output(f"Regex error on pair {i + 1}: {e}")

                        return

                else:

                    if self.case_cb.isChecked():

                        text = text.replace(f, r)

                    else:

                        text = re.sub(re.escape(f), r, text, flags=flags)



        self.set_output(text)



    def _count_matches(self):

        text = self.get_input()

        use_regex = self.regex_cb.isChecked()

        flags = self._get_flags()

        find = self.find_edit.text() if self.single_radio.isChecked() else ""

        if not find:

            self.set_output("Enter a search term first.")

            return

        try:

            if use_regex:

                count = len(re.findall(find, text, flags))

            else:

                count = len(re.findall(re.escape(find), text, flags))

        except re.error as e:

            self.set_output(f"Regex error: {e}")

            return

        self.set_output(f"Matches found: {count}")





# ═══════════════════════════════════════════════════════════════════════

# 7. Letter Case Converter

# ═══════════════════════════════════════════════════════════════════════

class LetterCaseConverterTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Letter Case Converter", parent)



    def build_controls(self, layout):

        row1 = QHBoxLayout()

        for label, func in [

            ("UPPER CASE", lambda: self.get_input().upper()),

            ("lower case", lambda: self.get_input().lower()),

            ("Sentence case.", self._sentence_case),

        ]:

            btn = QPushButton(label)

            btn.setObjectName("executeBtn")

            btn.clicked.connect(lambda _, f=func: self.set_output(f()))

            row1.addWidget(btn)

        layout.addLayout(row1)



        row2 = QHBoxLayout()

        for label, func in [

            ("Title Case", lambda: self.get_input().title()),

            ("tOGGLE cASE", lambda: self.get_input().swapcase()),

            ("AlTeRnAtInG CaSe", self._alternating_case),

        ]:

            btn = QPushButton(label)

            btn.setObjectName("executeBtn")

            btn.clicked.connect(lambda _, f=func: self.set_output(f()))

            row2.addWidget(btn)

        layout.addLayout(row2)



    def _sentence_case(self):

        text = self.get_input()

        return re.sub(r'((?:^|[.!?]\s+)\s*)(\w)', lambda m: m.group(1) + m.group(2).upper(),

                      text.lower())



    def _alternating_case(self):

        result = []

        upper = True

        for ch in self.get_input():

            if ch.isalpha():

                result.append(ch.upper() if upper else ch.lower())

                upper = not upper

            else:

                result.append(ch)

        return "".join(result)





# ═══════════════════════════════════════════════════════════════════════

# 8. Join / Merge Text (Line by Line)

# ═══════════════════════════════════════════════════════════════════════

class JoinMergeTextTool(BaseToolWidget):

    """This tool has its own two input areas, so we hide the default input."""



    def __init__(self, parent=None):

        super().__init__("Join / Merge Text (Line by Line)", parent)

        # Hide the default input/output — we use custom ones

        self.input_text.parent().hide()



    def build_controls(self, layout):

        splitter = QSplitter(Qt.Orientation.Horizontal)



        w1 = QWidget()

        l1 = QVBoxLayout(w1)

        l1.setContentsMargins(0, 0, 0, 0)

        l1.addWidget(QLabel("List 1"))

        self.list1 = QPlainTextEdit()

        l1.addWidget(self.list1)

        splitter.addWidget(w1)



        w2 = QWidget()

        l2 = QVBoxLayout(w2)

        l2.setContentsMargins(0, 0, 0, 0)

        l2.addWidget(QLabel("List 2"))

        self.list2 = QPlainTextEdit()

        l2.addWidget(self.list2)

        splitter.addWidget(w2)



        layout.addWidget(splitter, 1)



        form = QFormLayout()

        self.sep_edit = QLineEdit(" ")

        self.sep_edit.setObjectName("sep_edit")

        form.addRow("Separator:", self.sep_edit)

        layout.addLayout(form)



        # Mismatch handling

        grp = QGroupBox("When lists differ in length")

        gl = QVBoxLayout(grp)

        self.pad_radio = QRadioButton("Pad shorter list with empty strings")

        self.trunc_radio = QRadioButton("Truncate longer list")

        self.repeat_radio = QRadioButton("Repeat shorter list items")

        self.pad_radio.setChecked(True)

        self._mismatch_group = QButtonGroup()

        self._mismatch_group.addButton(self.pad_radio)

        self._mismatch_group.addButton(self.trunc_radio)

        self._mismatch_group.addButton(self.repeat_radio)

        gl.addWidget(self.pad_radio)

        gl.addWidget(self.trunc_radio)

        gl.addWidget(self.repeat_radio)

        layout.addWidget(grp)



        btn = QPushButton("▶ Merge Lists")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        a = self.list1.toPlainText().split("\n")

        b = self.list2.toPlainText().split("\n")

        sep = self.sep_edit.text()

        max_len = max(len(a), len(b))



        if self.trunc_radio.isChecked():

            max_len = min(len(a), len(b))

        elif self.repeat_radio.isChecked():

            if len(a) < max_len and a:

                a = [a[i % len(a)] for i in range(max_len)]

            if len(b) < max_len and b:

                b = [b[i % len(b)] for i in range(max_len)]



        result = []

        for i in range(max_len):

            va = a[i] if i < len(a) else ""

            vb = b[i] if i < len(b) else ""

            result.append(f"{va}{sep}{vb}")

        self.set_output("\n".join(result))





# ═══════════════════════════════════════════════════════════════════════

# 9. Remove Duplicate Lines

# ═══════════════════════════════════════════════════════════════════════

class RemoveDuplicateLinesTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Duplicate Lines", parent)



    def build_controls(self, layout):

        self.case_cb = QCheckBox("Case Sensitive Comparison")

        self.case_cb.setObjectName("case_cb")

        self.case_cb.setChecked(True)

        self.trim_cb = QCheckBox("Trim whitespace before comparing")

        self.trim_cb.setObjectName("trim_cb")

        self.keep_dupes_cb = QCheckBox("Keep Only Duplicates")

        self.keep_dupes_cb.setObjectName("keep_dupes_cb")

        layout.addWidget(self.case_cb)

        layout.addWidget(self.trim_cb)

        layout.addWidget(self.keep_dupes_cb)



        btn = QPushButton("▶ Process")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        lines = self.get_input().split("\n")

        case_sensitive = self.case_cb.isChecked()

        trim = self.trim_cb.isChecked()

        keep_only_dupes = self.keep_dupes_cb.isChecked()



        seen = {}

        for line in lines:

            key = line.strip() if trim else line

            if not case_sensitive:

                key = key.lower()

            seen[key] = seen.get(key, 0) + 1



        result = []

        seen_output = set()

        for line in lines:

            key = line.strip() if trim else line

            if not case_sensitive:

                key = key.lower()

            if keep_only_dupes:

                if seen[key] > 1 and key not in seen_output:

                    result.append(line)

                    seen_output.add(key)

            else:

                if key not in seen_output:

                    result.append(line)

                    seen_output.add(key)

        self.set_output("\n".join(result))





# ═══════════════════════════════════════════════════════════════════════

# 10. Remove Duplicate Words

# ═══════════════════════════════════════════════════════════════════════

class RemoveDuplicateWordsTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Duplicate Words", parent)



    def build_controls(self, layout):

        self.case_cb = QCheckBox("Case Sensitive Comparison")

        self.case_cb.setObjectName("case_cb")

        self.case_cb.setChecked(True)

        self.keep_dupes_cb = QCheckBox("Keep Only Duplicate Words")

        self.keep_dupes_cb.setObjectName("keep_dupes_cb")

        layout.addWidget(self.case_cb)

        layout.addWidget(self.keep_dupes_cb)



        btn = QPushButton("▶ Process")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        words = self.get_input().split()

        case_sensitive = self.case_cb.isChecked()

        keep_only = self.keep_dupes_cb.isChecked()



        count = {}

        for w in words:

            key = w if case_sensitive else w.lower()

            count[key] = count.get(key, 0) + 1



        seen = set()

        result = []

        for w in words:

            key = w if case_sensitive else w.lower()

            if keep_only:

                if count[key] > 1 and key not in seen:

                    result.append(w)

                    seen.add(key)

            else:

                if key not in seen:

                    result.append(w)

                    seen.add(key)

        self.set_output(" ".join(result))





# ═══════════════════════════════════════════════════════════════════════

# 11. Remove Empty Lines

# ═══════════════════════════════════════════════════════════════════════

class RemoveEmptyLinesTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Empty Lines", parent)



    def build_controls(self, layout):

        btn = QPushButton("▶ Remove Empty Lines")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        lines = self.get_input().split("\n")

        self.set_output("\n".join(l for l in lines if l.strip()))





# ═══════════════════════════════════════════════════════════════════════

# 12. Remove Extra Spaces

# ═══════════════════════════════════════════════════════════════════════

class RemoveExtraSpacesTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Extra Spaces", parent)



    def build_controls(self, layout):

        btn = QPushButton("▶ Remove Extra Spaces")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        lines = self.get_input().split("\n")

        result = [re.sub(r' +', ' ', line).strip() for line in lines]

        self.set_output("\n".join(result))





# ═══════════════════════════════════════════════════════════════════════

# 13. Remove Letter Accents

# ═══════════════════════════════════════════════════════════════════════

class RemoveLetterAccentsTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Letter Accents", parent)



    def build_controls(self, layout):

        btn = QPushButton("▶ Remove Accents")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        text = self.get_input()

        nfkd = unicodedata.normalize('NFKD', text)

        result = "".join(c for c in nfkd if not unicodedata.combining(c))

        self.set_output(result)





# ═══════════════════════════════════════════════════════════════════════

# 14. Remove Lines Containing

# ═══════════════════════════════════════════════════════════════════════

class RemoveLinesContainingTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Lines Containing", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.match_edit = QLineEdit()

        self.match_edit.setObjectName("match_edit")

        self.match_edit.setPlaceholderText("Text or /regex/ to match")

        form.addRow("Match:", self.match_edit)

        layout.addLayout(form)



        # Export mode

        mode_row = QHBoxLayout()

        self.export_containing = QRadioButton("Export Lines Containing")

        self.export_not_containing = QRadioButton("Export Lines NOT Containing")

        self.export_not_containing.setChecked(True)

        self._mode_grp = QButtonGroup()

        self._mode_grp.addButton(self.export_containing)

        self._mode_grp.addButton(self.export_not_containing)

        mode_row.addWidget(self.export_containing)

        mode_row.addWidget(self.export_not_containing)

        layout.addLayout(mode_row)



        self.case_cb = QCheckBox("Case Sensitive")

        self.case_cb.setObjectName("case_cb")

        self.whole_word_cb = QCheckBox("Match Whole Word Only")

        self.whole_word_cb.setObjectName("whole_word_cb")

        self.regex_cb = QCheckBox("Use Regular Expression")

        self.regex_cb.setObjectName("regex_cb")

        layout.addWidget(self.case_cb)

        layout.addWidget(self.whole_word_cb)

        layout.addWidget(self.regex_cb)



        btn = QPushButton("▶ Process")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        text = self.get_input()

        pattern = self.match_edit.text()

        if not pattern:

            return

        case = self.case_cb.isChecked()

        whole_word = self.whole_word_cb.isChecked()

        use_regex = self.regex_cb.isChecked()

        export_matching = self.export_containing.isChecked()

        flags = 0 if case else re.IGNORECASE



        if use_regex:

            try:

                pat = re.compile(pattern, flags)

            except re.error as e:

                self.set_output(f"Regex error: {e}")

                return

        elif whole_word:

            pat = re.compile(r'\b' + re.escape(pattern) + r'\b', flags)

        else:

            pat = re.compile(re.escape(pattern), flags)



        result = []

        for line in text.split("\n"):

            match = pat.search(line)

            if export_matching and match:

                result.append(line)

            elif not export_matching and not match:

                result.append(line)

        self.set_output("\n".join(result))





# ═══════════════════════════════════════════════════════════════════════

# 15. Remove Punctuation

# ═══════════════════════════════════════════════════════════════════════

class RemovePunctuationTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Punctuation", parent)



    def build_controls(self, layout):

        btn = QPushButton("▶ Remove Punctuation")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        import string

        text = self.get_input()

        result = text.translate(str.maketrans('', '', string.punctuation))

        self.set_output(result)





# ═══════════════════════════════════════════════════════════════════════

# 16. Sort Text Lines

# ═══════════════════════════════════════════════════════════════════════

class SortTextLinesTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Sort Text Lines", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.sort_combo = QComboBox()

        self.sort_combo.setObjectName("sort_combo")

        self.sort_combo.addItems([

            "Alphabetical (A → Z)", "Alphabetical (Z → A)",

            "Numeric (Low → High)", "Numeric (High → Low)",

            "Natural Sort (Asc)", "Natural Sort (Desc)",

            "Length (Short → Long)", "Length (Long → Short)",

            "Reverse Line Order"

        ])

        form.addRow("Sort Type:", self.sort_combo)

        layout.addLayout(form)



        self.case_cb = QCheckBox("Case Sensitive Sort")

        self.case_cb.setObjectName("case_cb")

        layout.addWidget(self.case_cb)



        btn = QPushButton("▶ Sort Lines")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _natural_key(self, s):

        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]



    def _execute(self):

        lines = self.get_input().split("\n")

        case = self.case_cb.isChecked()

        idx = self.sort_combo.currentIndex()



        if idx == 0:  # Alpha Asc

            lines.sort(key=lambda x: x if case else x.lower())

        elif idx == 1:  # Alpha Desc

            lines.sort(key=lambda x: x if case else x.lower(), reverse=True)

        elif idx == 2:  # Numeric Asc

            lines.sort(key=lambda x: self._safe_float(x))

        elif idx == 3:  # Numeric Desc

            lines.sort(key=lambda x: self._safe_float(x), reverse=True)

        elif idx == 4:  # Natural Asc

            lines.sort(key=self._natural_key)

        elif idx == 5:  # Natural Desc

            lines.sort(key=self._natural_key, reverse=True)

        elif idx == 6:  # Length Asc

            lines.sort(key=len)

        elif idx == 7:  # Length Desc

            lines.sort(key=len, reverse=True)

        elif idx == 8:  # Reverse

            lines.reverse()



        self.set_output("\n".join(lines))



    @staticmethod

    def _safe_float(s):

        try:

            return float(re.sub(r'[^\d.\-]', '', s))

        except (ValueError, TypeError):

            return float('inf')





# ═══════════════════════════════════════════════════════════════════════
# 17. Remove Line Numbers

# ═══════════════════════════════════════════════════════════════════════

class RemoveLineNumbersTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Remove Line Numbers", parent)



    def build_controls(self, layout):

        self.keep_space_cb = QCheckBox("Keep single leading space after removing number")

        self.keep_space_cb.setObjectName("keep_space_cb")

        layout.addWidget(self.keep_space_cb)



        btn = QPushButton("▶ Remove Line Numbers")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        lines = self.get_input().split("\n")

        keep_space = self.keep_space_cb.isChecked()

        result = []

        for line in lines:

            cleaned = re.sub(r'^\s*\d+[\.\)\:\-]?\s?', ' ' if keep_space else '', line)

            result.append(cleaned)

        self.set_output("\n".join(result))





# ═══════════════════════════════════════════════════════════════════════
# 18. Alphabetize Text

# ═══════════════════════════════════════════════════════════════════════

class AlphabetizeTextTool(BaseToolWidget):

    def __init__(self, parent=None):

        super().__init__("Alphabetize Text", parent)



    def build_controls(self, layout):

        form = QFormLayout()

        self.method_combo = QComboBox()

        self.method_combo.setObjectName("method_combo")

        self.method_combo.addItems(["Sort Lines", "Sort Words", "Sort Delimited Items"])

        form.addRow("Sort Method:", self.method_combo)



        self.delim_edit = QLineEdit("")

        self.delim_edit.setObjectName("delim_edit")

        self.delim_edit.setPlaceholderText("Delimiter (for 'Delimited Items' mode)")

        form.addRow("Delimiter:", self.delim_edit)

        layout.addLayout(form)



        self.order_combo = QComboBox()

        self.order_combo.setObjectName("order_combo")

        self.order_combo.addItems(["A → Z (Ascending)", "Z → A (Descending)"])

        layout.addWidget(QLabel("Sort Order:"))

        layout.addWidget(self.order_combo)



        self.case_cb = QCheckBox("Case Sensitive")

        self.case_cb.setObjectName("case_cb")

        self.remove_dupes_cb = QCheckBox("Remove Duplicates")

        self.remove_dupes_cb.setObjectName("remove_dupes_cb")

        layout.addWidget(self.case_cb)

        layout.addWidget(self.remove_dupes_cb)



        btn = QPushButton("▶ Alphabetize")

        btn.setObjectName("executeBtn")

        btn.clicked.connect(self._execute)

        layout.addWidget(btn)



    def _execute(self):

        text = self.get_input()

        method = self.method_combo.currentIndex()

        delim = self.delim_edit.text()

        case = self.case_cb.isChecked()

        dupes = self.remove_dupes_cb.isChecked()

        desc = self.order_combo.currentIndex() == 1



        if method == 0:  # Lines

            items = text.split("\n")

            joiner = "\n"

        elif method == 1:  # Words

            items = re.split(r'\s+', text)

            joiner = " "

        else:  # Delimited

            items = text.split(delim)

            joiner = delim



        # Clean items (remove empty if words)

        if method == 1:

            items = [i for i in items if i.strip()]



        if dupes:

            seen = set()

            new_items = []

            for i in items:

                key = i if case else i.lower()

                if key not in seen:

                    new_items.append(i)

                    seen.add(key)

            items = new_items



        items.sort(key=lambda x: x if case else x.lower(), reverse=desc)

        self.set_output(joiner.join(items))

