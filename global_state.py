"""
Global state manager for sharing text between tools.
Provides a singleton for 'last result' and 'notepad text' sharing.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class GlobalState(QObject):
    """Singleton that holds shared application state."""

    _instance = None
    _is_init = False

    last_result_changed = pyqtSignal(str)
    notepad_text_changed = pyqtSignal(str)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GlobalState._is_init:
            return
        super().__init__()
        GlobalState._is_init = True
        self._last_result = ""
        self._notepad_text = ""

    @property
    def last_result(self) -> str:
        return self._last_result

    @last_result.setter
    def last_result(self, value: str):
        self._last_result = value
        self.last_result_changed.emit(value)

    @property
    def notepad_text(self) -> str:
        return self._notepad_text

    @notepad_text.setter
    def notepad_text(self, value: str):
        self._notepad_text = value
        self.notepad_text_changed.emit(value)
