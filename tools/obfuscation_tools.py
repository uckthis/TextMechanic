"""
Category 4: Obfuscation & Encoding (FULLY IMPLEMENTED)
Tools: Binary Translator, Base64 Encode/Decode, Disemvowel,
       Reverse Text, ROT13 Cipher, Word Scrambler.
"""

import base64
import codecs
import random
import re

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
)
from base_tool import BaseToolWidget


# ═══════════════════════════════════════════════════════════════════════
# 1. Binary Code Translator
# ═══════════════════════════════════════════════════════════════════════
class BinaryTranslatorTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Binary Code Translator", parent)

    def build_controls(self, layout):
        row = QHBoxLayout()
        btn_to_bin = QPushButton("▶ Text → Binary")
        btn_to_bin.setObjectName("executeBtn")
        btn_to_text = QPushButton("▶ Binary → Text")
        btn_to_text.setObjectName("executeBtn")
        btn_to_bin.clicked.connect(self._to_binary)
        btn_to_text.clicked.connect(self._to_text)
        row.addWidget(btn_to_bin)
        row.addWidget(btn_to_text)
        layout.addLayout(row)

    def _to_binary(self):
        text = self.get_input()
        binary = " ".join(f"{b:08b}" for b in text.encode('utf-8'))
        self.set_output(binary)

    def _to_text(self):
        text = self.get_input().strip()
        try:
            chunks = text.split()
            byte_arr = bytes(int(b, 2) for b in chunks)
            self.set_output(byte_arr.decode('utf-8'))
        except (ValueError, UnicodeDecodeError) as e:
            self.set_output(f"Error: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 2. Base64 Encode / Decode
# ═══════════════════════════════════════════════════════════════════════
class Base64EncoderTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Base64 Encode / Decode", parent)

    def build_controls(self, layout):
        self.url_safe_cb = QCheckBox("Use URL Safe Alphabet")
        self.url_safe_cb.setObjectName("url_safe_cb")
        self.omit_padding_cb = QCheckBox("Omit Padding (=)")
        self.omit_padding_cb.setObjectName("omit_padding_cb")
        layout.addWidget(self.url_safe_cb)
        layout.addWidget(self.omit_padding_cb)

        row = QHBoxLayout()
        btn_encode = QPushButton("▶ Encode")
        btn_encode.setObjectName("executeBtn")
        btn_decode = QPushButton("▶ Decode")
        btn_decode.setObjectName("executeBtn")
        btn_encode.clicked.connect(self._encode)
        btn_decode.clicked.connect(self._decode)
        row.addWidget(btn_encode)
        row.addWidget(btn_decode)
        layout.addLayout(row)

    def _encode(self):
        data = self.get_input().encode('utf-8')
        if self.url_safe_cb.isChecked():
            encoded = base64.urlsafe_b64encode(data).decode('ascii')
        else:
            encoded = base64.b64encode(data).decode('ascii')
        if self.omit_padding_cb.isChecked():
            encoded = encoded.rstrip('=')
        self.set_output(encoded)

    def _decode(self):
        text = self.get_input().strip()
        # Restore padding if omitted
        padding = 4 - len(text) % 4
        if padding != 4:
            text += '=' * padding
        try:
            if self.url_safe_cb.isChecked():
                decoded = base64.urlsafe_b64decode(text).decode('utf-8')
            else:
                decoded = base64.b64decode(text).decode('utf-8')
            self.set_output(decoded)
        except Exception as e:
            self.set_output(f"Error: {e}")


# ═══════════════════════════════════════════════════════════════════════
# 3. Disemvowel Tool
# ═══════════════════════════════════════════════════════════════════════
class DisemvowelTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Disemvowel Tool", parent)

    def build_controls(self, layout):
        self.keep_y_cb = QCheckBox("Keep 'Y' and 'y'")
        self.keep_y_cb.setObjectName("keep_y_cb")
        layout.addWidget(self.keep_y_cb)

        btn = QPushButton("▶ Disemvowel")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        text = self.get_input()
        vowels = set("aeiouAEIOU")
        if not self.keep_y_cb.isChecked():
            vowels.update("yY")
        result = "".join(ch for ch in text if ch not in vowels)
        self.set_output(result)


# ═══════════════════════════════════════════════════════════════════════
# 4. Reverse Text
# ═══════════════════════════════════════════════════════════════════════
class ReverseTextTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Reverse Text", parent)

    def build_controls(self, layout):
        for label, func in [
            ("Reverse Entire Text", self._reverse_all),
            ("Reverse Letters within Words", self._reverse_words_letters),
            ("Reverse Word Order per Line", self._reverse_word_order),
            ("Reverse Order of Lines", self._reverse_lines),
        ]:
            btn = QPushButton(f"▶ {label}")
            btn.setObjectName("executeBtn")
            btn.clicked.connect(func)
            layout.addWidget(btn)

    def _reverse_all(self):
        self.set_output(self.get_input()[::-1])

    def _reverse_words_letters(self):
        text = self.get_input()
        result = re.sub(r'\S+', lambda m: m.group()[::-1], text)
        self.set_output(result)

    def _reverse_word_order(self):
        lines = self.get_input().split("\n")
        result = [" ".join(line.split()[::-1]) for line in lines]
        self.set_output("\n".join(result))

    def _reverse_lines(self):
        lines = self.get_input().split("\n")
        self.set_output("\n".join(reversed(lines)))


# ═══════════════════════════════════════════════════════════════════════
# 5. ROT13 Cipher
# ═══════════════════════════════════════════════════════════════════════
class ROT13Tool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("ROT13 Cipher", parent)

    def build_controls(self, layout):
        btn = QPushButton("▶ Apply ROT13")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        self.set_output(codecs.encode(self.get_input(), 'rot_13'))


# ═══════════════════════════════════════════════════════════════════════
# 6. Word Scrambler
# ═══════════════════════════════════════════════════════════════════════
class WordScramblerTool(BaseToolWidget):
    def __init__(self, parent=None):
        super().__init__("Word Scrambler", parent)

    def build_controls(self, layout):
        self.keep_ends_cb = QCheckBox("Keep First and Last Letter Intact")
        self.keep_ends_cb.setObjectName("keep_ends_cb")
        self.keep_ends_cb.setChecked(True)
        layout.addWidget(self.keep_ends_cb)

        btn = QPushButton("▶ Scramble Words")
        btn.setObjectName("executeBtn")
        btn.clicked.connect(self._execute)
        layout.addWidget(btn)

    def _execute(self):
        text = self.get_input()
        keep_ends = self.keep_ends_cb.isChecked()

        def scramble_word(w):
            if len(w) <= 3:
                return w
            if keep_ends:
                middle = list(w[1:-1])
                random.shuffle(middle)
                return w[0] + "".join(middle) + w[-1]
            else:
                chars = list(w)
                random.shuffle(chars)
                return "".join(chars)

        result = re.sub(r'[A-Za-z]+', lambda m: scramble_word(m.group()), text)
        self.set_output(result)
