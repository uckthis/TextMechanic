# Text Mechanic

A modern, fast desktop toolbox for transforming, cleaning, and analyzing text.
Built with Python + PyQt6.

![Version](https://img.shields.io/badge/version-1.1.2-orange)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)

---

## Features

- **43 tools across 8 categories** — prefix/suffix, case conversion, sort, dedupe, extract, encode, randomize, combine, and more
- **5 hand-crafted themes** — Daylight, Dark, Sunset, Blush, Forest
- **Live tool previews** — see what your input looks like as you tweak settings
- **Drag-and-drop** — drop `.txt`, `.csv`, `.json`, `.md`, `.log` files onto any input
- **Chain tools** — "Use Last Result" pipes one tool's output into the next
- **Notepad with pipeline** — queue up to 20 operations and run them in sequence
- **Frequently Used** — your most-used tools surface on the home dashboard automatically
- **Persistent settings** — theme, window size, expanded categories, per-tool state, all saved
- **Modern minimal UI** — clean type, generous spacing, refined color tokens

## Screenshots
<img width="3840" height="2160" alt="1" src="https://github.com/user-attachments/assets/13bb2de8-6447-4bee-b793-a34dca1b2913" />
<img width="3840" height="2160" alt="2" src="https://github.com/user-attachments/assets/e0d05a08-6d32-45db-96d8-25509e25fc3a" />


## Download

Grab the latest release from the [Releases](../../releases) page — single-file
Windows installer, no Python required.

## Run from source

```powershell
# Requires Python 3.10+
pip install -r requirements.txt
python main.py
```

## Build the executable

```powershell
pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean TextMechanic.spec
# Output: dist\TextMechanic-<version>.exe
```

## Project structure

```
.
├── main.py                # Application entry point, MainWindow, WelcomeDashboard
├── base_tool.py           # BaseToolWidget (page header, IO cards, action bar)
├── theme_manager.py       # 5 themes + QSS template (used to generate stylesheets)
├── global_state.py        # Cross-tool state (last result, notepad text)
├── version.py             # Single source of truth for app version
├── icon.png               # App icon (used for both QSS and PyInstaller)
├── TextMechanic.spec      # PyInstaller build config
├── tools/
│   ├── basic_text_tools.py     # Basic Text Tools (18 tools)
│   ├── extraction_tools.py     # Extraction & Analysis (2 tools)
│   ├── format_web_tools.py     # Format & Web Tools (5 tools)
│   ├── obfuscation_tools.py    # Obfuscation & Encoding (6 tools)
│   ├── randomization_tools.py  # Randomization (4 tools)
│   ├── combination_tools.py    # Combination / Permutation (4 tools)
│   ├── numeration_tools.py     # Numeration (3 tools)
│   └── allinone_tools.py       # Notepad (1 tool with 20 operations)
├── requirements.txt
├── LICENSE
└── README.md
```

## Themes

Switch themes from the dropdown in the top bar. Each theme is a palette of
16 color tokens defined in `theme_manager.py`. The QSS template substitutes
those tokens to produce the full stylesheet — no per-tool styling needed.

| Theme | Mode | Accent |
|---|---|---|
| Daylight | light | amber |
| Dark | dark | amber |
| Sunset | light | orange |
| Blush | light | pink |
| Forest | dark | emerald |

## Adding a new tool

1. Add a `class YourTool(BaseToolWidget)` in the appropriate file under `tools/`
2. Override `build_controls(self, layout)` to add tool-specific controls
3. Use the standard `self.input_text` and `self.output_text` (provided by `BaseToolWidget`)
4. Call `self.set_output(your_result_text)` to fill the output
5. Register the tool in `TOOL_REGISTRY` in `main.py`
6. (Optional) Add a card-friendly entry in `TOOL_INFO` for the welcome dashboard

The tool will automatically inherit the page header, IO section, action bar,
and theme styling.

## Versioning

`version.py` is the single source of truth. Format: `MAJOR.MINOR.PATCH`

- **MAJOR** — breaking UI changes or removed features
- **MINOR** — new tools, new themes, new layouts
- **PATCH** — bug fixes, polish, no behavior change

Bump it and rebuild — the title bar, status bar, and exe filename all update.

## License

MIT — see [LICENSE](LICENSE).
