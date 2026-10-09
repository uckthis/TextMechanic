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

## Tools

A short description of every tool, grouped by category. Every tool works on text in place — copy in, tweak the controls, copy out. No upload, no server, fully local.

### Basic Text Tools (18)

- **Add Prefix / Suffix / Delimiter** — Insert a label, suffix, or delimiter (comma, newline, bracket, anything) at the start or end of every line.
- **Add / Remove Line Breaks** — Insert or strip line breaks at fixed character positions or after regex matches.
- **Add Repeats** — Duplicate each line N times, with an option to skip the original and only emit repeats.
- **Count Characters, Words, etc.** — Total characters, words, sentences, paragraphs and reading-time stats at once.
- **Split Text by Delimiter** — Break text into rows and columns using any delimiter (comma, tab, pipe, regex), with live column preview.
- **Find and Replace Text** — Plain or regex find-and-replace with case, whole-word, multiline and per-line modes.
- **Letter Case Converter** — title case, UPPER, lower, Sentence case, camelCase, snake_case, kebab-case and more.
- **Join / Merge Text (Line by Line)** — Zip two lists into one — line 1 of A + line 1 of B + separator — or merge with a smart `min/max` blend.
- **Remove Duplicate Lines** — Keep first, keep last, or uniques only, with case-sensitive and whitespace-trim options.
- **Remove Duplicate Words** — Drop repeated words inside each line or across the whole document.
- **Remove Empty Lines** — Strip blank lines, optionally also trimming whitespace-only lines.
- **Remove Extra Spaces** — Collapse runs of spaces and tabs into a single space, plus leading/trailing trim.
- **Remove Letter Accents** — Strip diacritics: `é → e`, `ñ → n`, `ö → o` — great for slugifying names or normalizing.
- **Remove Lines Containing** — Drop lines that match a substring or regex (positive or negative match).
- **Remove Punctuation** — Strip punctuation with a configurable allow-list (keep hyphens? apostrophes? slashes? etc.).
- **Sort Text Lines** — Sort ascending, descending, by length, randomly, or by line numbers — with locale-aware handling.
- **Remove Line Numbers** — Strip leading `1. `, `01) `, `a)` etc. numeric or alphabetic prefixes from each line.
- **Alphabetize Text** — Pure alphabetical sort across lines (locale-aware, ignores case and diacritics).

### Extraction & Analysis (2)

- **Extract Text Between Strings** — Pull out everything between an opening and a closing marker — HTML tags, parens, brackets, quotes.
- **Word Frequency Counter** — Rank every word by occurrence count with case, length and stopword filters; export the table.

### Format & Web Tools (5)

- **ASCII / Unicode Converter** — Show the Unicode codepoints, JSON escapes and ASCII bytes for any text — round-trip in either direction.
- **Convert Timestamp** — Epoch ⇄ human-readable date/time across ISO, RFC, custom strftime and timezone-aware formats.
- **Diff Checker (Text Compare)** — Side-by-side diff of two inputs with line-level and word-level highlighting.
- **Regex Tester / Matcher** — Live regex tester with match highlighting, capture groups and replacement preview.
- **Hex Encoder / Decoder** — Convert text to hex (and back) with configurable spacing, separator, prefix (`0x`) and line-wrap.

### Obfuscation & Encoding (6)

- **Binary Code Translator** — text ⇄ 8-bit binary strings, with optional spacing, grouping, and MSB/LSB order.
- **Base64 Encode / Decode** — Encode to Base64 or decode from Base64, with URL-safe alphabet option.
- **Disemvowel Tool** — Strip vowels (or any custom character set) from text — fun for codetalk-style obfuscation.
- **Reverse Text** — Reverse characters, words (each line), or the entire document character-by-character.
- **ROT13 Cipher** — Rotate letters by N (defaults to ROT13) — handles lowercase, uppercase, and Unicode letters.
- **Word Scrambler** — Shuffle the letters inside each word while leaving the first/last letter fixed (configurable).

### Randomization Tools (4)

- **Random Line Picker** — Pull N random lines from the input; supports no-repeats, seedable shuffle, weighted pick.
- **Random Number Generator** — Generate integers or floats in a range, with optional uniqueness, sort, separator and seed.
- **Random String Generator** — Produce passwords / tokens of given length and character set (upper, lower, digits, symbols).
- **String Randomizer** — Shuffle the entire input's characters at random — perfect for visual/text fuzzing.

### Combination / Permutation (4)

- **Combination Generator (nCk)** — Generate every subset of size `k` from a list (input as CSV).
- **Lists Comparison Tool** — Compute A∩B, A∪B, A−B, B−A, or symmetric difference between any two lists.
- **Line Combination Generator** — Build every combination of `n` rows deep — great for synthetic test data.
- **Permutation Generator (n!)** — Generate every ordering of `n` lines, with a max-output cap to avoid explosions.

### Numeration Tools (3)

- **Generate List of Numbers** — Range generator: `1` to `100`, every `5`th, in reverse, zero-padded, signed, prefixed — anything.
- **Number Each Line** — Prefix every line with a counter in your format — `1. `, `01) `, `(1) `, `[1] `, custom template.
- **Online Tally Counter** — Click-up live tally with named counters, undo, save-to-file — useful for streaming/manual counts.

### All-in-One (1)

- **Text Manipulation Notepad** — A scratchpad with a left rail of every operation; queue up to 20 ops, run in order, watch live stats (chars/words/lines) update as you type.

## Screenshots

*Coming soon — drop a screenshot in `docs/` and reference it here.*

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
