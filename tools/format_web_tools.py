"""
Category 3: Format & Web Tools (FULLY IMPLEMENTED)
Tools: ASCII/Unicode Converter, Convert Timestamp, Diff Checker,
       Regex Tester / Matcher, Hex Encoder/Decoder.
"""

import re
import difflib
from datetime import datetime, timezone

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QRadioButton, QSpinBox, QButtonGroup,
    QPlainTextEdit, QGroupBox, QWidget, QSplitter, QDateTimeEdit,
    QApplication
)
from PyQt6.QtCore import Qt, QDateTime
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. ASCII / Unicode Converter
# ═══════════════════════════════════════════════════════════════════════
class AsciiUnicodeConverterTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("ASCII / Unicode Converter", parent)

    def build_controls(self, layout):
        row = QHBoxLayout()
        btn_to_unicode = QPushButton("▶ Text → Unicode Code Points")
        btn_to_unicode.setObjectName("executeBtn")
        btn_to_text = QPushButton("▶ Unicode Code Points → Text")
        btn_to_text.setObjectName("executeBtn")
        btn_to_unicode.clicked.connect(self._to_unicode)
        btn_to_text.clicked.connect(self._to_text)
        row.addWidget(btn_to_unicode)
        row.addWidget(btn_to_text)
        layout.addLayout(row)

    def _to_unicode(self):
        text = self.get_input()
        result = " ".join(f"U+{ord(ch):04X}" for ch in text)
        self.set_output(result)

    def _to_text(self):
        text = self.get_input().strip()
        try:
            chars = []
            for token in text.split():
                token = token.strip().upper()
                if token.startswith("U+"):
                    token = token[2:]
                chars.append(chr(int(token, 16)))
            self.set_output("".join(chars))
        except (ValueError, OverflowError) as e:
            self.set_output(f"Error: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 2. Convert Timestamp
# ═══════════════════════════════════════════════════════════════════════
class ConvertTimestampTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Convert Timestamp", parent)
        # Hide default input/output — this tool uses custom controls
        self.input_text.parent().hide()

    def build_controls(self, layout):
        form = QFormLayout()

        self.unix_edit = QLineEdit()
        self.unix_edit.setObjectName("unix_edit")
        self.unix_edit.setPlaceholderText("e.g. 1700000000")
        form.addRow("Unix Timestamp:", self.unix_edit)

        self.dt_edit = QDateTimeEdit()
        self.dt_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dt_edit.setCalendarPopup(True)
        self.dt_edit.setDateTime(QDateTime.currentDateTime())
        form.addRow("Human Date/Time:", self.dt_edit)

        self.ms_cb = QCheckBox("Input is Milliseconds")
        self.ms_cb.setObjectName("ms_cb")
        form.addRow("", self.ms_cb)
        layout.addLayout(form)

        row = QHBoxLayout()
        btn1 = QPushButton("▶ Convert to Human Date")
        btn1.setObjectName("executeBtn")
        btn2 = QPushButton("▶ Convert to Unix Timestamp")
        btn2.setObjectName("executeBtn")
        btn1.clicked.connect(self._to_human)
        btn2.clicked.connect(self._to_unix)
        row.addWidget(btn1)
        row.addWidget(btn2)
        layout.addLayout(row)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet(
            "font-size:16px; font-weight:bold; color:#a6e3a1; padding:10px;"
        )
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.result_label)

    def _to_human(self):
        try:
            val = float(self.unix_edit.text())
            if self.ms_cb.isChecked():
                val /= 1000.0
            dt = datetime.fromtimestamp(val, tz=timezone.utc)
            result = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            self.result_label.setText(f"Human Date:  {result}")
            self.set_output(result)
        except (ValueError, OSError) as e:
            self.result_label.setText(f"Error: {e}")

    def _to_unix(self):
        qdt = self.dt_edit.dateTime()
        epoch = qdt.toSecsSinceEpoch()
        if self.ms_cb.isChecked():
            epoch *= 1000
        self.result_label.setText(f"Unix Timestamp:  {epoch}")
        self.set_output(str(epoch))


# ═══════════════════════════════════════════════════════════════════════
# 3. Diff Checker (Text Compare)
# ═══════════════════════════════════════════════════════════════════════
class DiffCheckerTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Diff Checker (Text Compare)", parent)
        self.input_text.parent().hide()

    def build_controls(self, layout):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        w1 = QWidget()
        l1 = QVBoxLayout(w1)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(QLabel("Text A"))
        self.text_a = QPlainTextEdit()
        self.text_a.setObjectName("text_a")
        l1.addWidget(self.text_a)
        splitter.addWidget(w1)

        w2 = QWidget()
        l2 = QVBoxLayout(w2)
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addWidget(QLabel("Text B"))
        self.text_b = QPlainTextEdit()
        self.text_b.setObjectName("text_b")
        l2.addWidget(self.text_b)
        splitter.addWidget(w2)

        layout.addWidget(splitter, 1)

        opts = QHBoxLayout()
        grp = QGroupBox("Compare By")
        gl = QHBoxLayout(grp)
        self.by_lines = QRadioButton("Lines")
        self.by_words = QRadioButton("Words")
        self.by_chars = QRadioButton("Characters")
        self.by_lines.setChecked(True)
        self._cmp_grp = QButtonGroup()
        self._cmp_grp.addButton(self.by_lines)
        self._cmp_grp.addButton(self.by_words)
        self._cmp_grp.addButton(self.by_chars)
        gl.addWidget(self.by_lines)
        gl.addWidget(self.by_words)
        gl.addWidget(self.by_chars)
        opts.addWidget(grp)

        self.ignore_case_cb = QCheckBox("Ignore Case")
        self.ignore_case_cb.setObjectName("ignore_case_cb")
        opts.addWidget(self.ignore_case_cb)
        layout.addLayout(opts)

        btn = QPushButton("▶ Compare")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        a = self.text_a.toPlainText()
        b = self.text_b.toPlainText()
        if self.ignore_case_cb.isChecked():
            a = a.lower()
            b = b.lower()

        if self.by_lines.isChecked():
            seq_a = a.splitlines(keepends=True)
            seq_b = b.splitlines(keepends=True)
            diff = difflib.unified_diff(seq_a, seq_b, fromfile="Text A",
                                        tofile="Text B", lineterm="")
        elif self.by_words.isChecked():
            seq_a = a.split()
            seq_b = b.split()
            diff = difflib.unified_diff(seq_a, seq_b, fromfile="Text A",
                                        tofile="Text B", lineterm="")
        else:
            seq_a = list(a)
            seq_b = list(b)
            diff = difflib.unified_diff(seq_a, seq_b, fromfile="Text A",
                                        tofile="Text B", lineterm="")

        result = "\n".join(diff)
        if not result.strip():
            result = "✅ The texts are identical."
        self.set_output(result)


# ═══════════════════════════════════════════════════════════════════════
# 4. Regex Tester / Matcher
# ═══════════════════════════════════════════════════════════════════════
class RegexTesterTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Regex Tester / Matcher", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.regex_edit = QLineEdit()
        self.regex_edit.setObjectName("regex_edit")
        self.regex_edit.setPlaceholderText("Regular expression…")
        self.flags_edit = QLineEdit()
        self.flags_edit.setObjectName("flags_edit")
        self.flags_edit.setPlaceholderText("Flags (e.g. i, m, s)")
        form.addRow("Pattern:", self.regex_edit)
        form.addRow("Flags:", self.flags_edit)
        layout.addLayout(form)

        btn_match = QPushButton("▶ Find Matches")
        btn_match.setObjectName("executeBtn")
        btn_match.clicked.connect(self._find_matches)
        layout.addWidget(btn_match)

        layout.addWidget(QLabel("Match Details"))
        self.match_details = QPlainTextEdit()
        self.match_details.setReadOnly(True)
        self.match_details.setMaximumHeight(120)
        layout.addWidget(self.match_details)

        # Test Replace sub-tool
        grp = QGroupBox("Test Replace")
        gl = QVBoxLayout(grp)
        form2 = QFormLayout()
        self.replace_edit = QLineEdit()
        self.replace_edit.setObjectName("replace_edit")
        form2.addRow("Replacement:", self.replace_edit)
        gl.addLayout(form2)
        btn_replace = QPushButton("▶ Test Replace")
        btn_replace.setObjectName("executeBtn")
        btn_replace.clicked.connect(self._test_replace)
        gl.addWidget(btn_replace)
        self.replace_output = QPlainTextEdit()
        self.replace_output.setReadOnly(True)
        self.replace_output.setMaximumHeight(100)
        gl.addWidget(self.replace_output)
        layout.addWidget(grp)

    def _parse_flags(self):
        flags = 0
        for ch in self.flags_edit.text().lower():
            if ch == 'i':
                flags |= re.IGNORECASE
            elif ch == 'm':
                flags |= re.MULTILINE
            elif ch == 's':
                flags |= re.DOTALL
            elif ch == 'x':
                flags |= re.VERBOSE
        return flags

    def _find_matches(self):
        text = self.get_input()
        pattern = self.regex_edit.text()
        if not pattern:
            return
        try:
            flags = self._parse_flags()
            matches = list(re.finditer(pattern, text, flags))
        except re.error as e:
            self.set_output(f"Regex error: {e}")
            return

        if not matches:
            self.set_output("No matches found.")
            self.match_details.setPlainText("")
            return

        highlighted = []
        details = []
        for i, m in enumerate(matches):
            highlighted.append(f"Match {i + 1}: \"{m.group()}\" "
                               f"(pos {m.start()}–{m.end()})")
            if m.groups():
                for j, g in enumerate(m.groups(), 1):
                    details.append(f"  Match {i + 1}, Group {j}: \"{g}\"")

        self.set_output("\n".join(highlighted))
        self.match_details.setPlainText(
            "\n".join(details) if details else "No capture groups."
        )

    def _test_replace(self):
        text = self.get_input()
        pattern = self.regex_edit.text()
        repl = self.replace_edit.text()
        if not pattern:
            return
        try:
            flags = self._parse_flags()
            result = re.sub(pattern, repl, text, flags=flags)
            self.replace_output.setPlainText(result)
        except re.error as e:
            self.replace_output.setPlainText(f"Regex error: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 5. Hex Encoder / Decoder
# ═══════════════════════════════════════════════════════════════════════
class HexEncoderDecoderTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Hex Encoder / Decoder", parent)

    def build_controls(self, layout):
        form = QFormLayout()
        self.sep_edit = QLineEdit(" ")
        form.addRow("Hex Output Separator:", self.sep_edit)
        layout.addLayout(form)

        row = QHBoxLayout()
        btn_encode = QPushButton("▶ Text → Hex")
        btn_encode.setObjectName("executeBtn")
        btn_decode = QPushButton("▶ Hex → Text")
        btn_decode.setObjectName("executeBtn")
        btn_encode.clicked.connect(self._to_hex)
        btn_decode.clicked.connect(self._to_text)
        row.addWidget(btn_encode)
        row.addWidget(btn_decode)
        layout.addLayout(row)

    def _to_hex(self):
        text = self.get_input()
        sep = self.sep_edit.text()
        hex_vals = [f"{b:02X}" for b in text.encode('utf-8')]
        self.set_output(sep.join(hex_vals))

    def _to_text(self):
        text = self.get_input().strip()
        try:
            # Try to handle various separator styles
            cleaned = re.sub(r'[^0-9a-fA-F]', ' ', text)
            hex_vals = cleaned.split()
            byte_arr = bytes(int(h, 16) for h in hex_vals)
            self.set_output(byte_arr.decode('utf-8'))
        except (ValueError, UnicodeDecodeError) as e:
            self.set_output(f"Error: {e}")
