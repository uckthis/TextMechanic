# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for Text Mechanic.
Reads version metadata from version.py and embeds it in the EXE name.
"""

import os
import sys

# Make `version` importable when PyInstaller runs this spec
spec_dir = os.path.abspath(os.path.dirname(os.path.abspath('TextMechanic.spec')) if 'TextMechanic.spec' in os.listdir('.') else os.getcwd())
sys.path.insert(0, spec_dir)

try:
    import version as v
except Exception:
    class v:
        __version__ = "0.0.0"
        __app_name__ = "Text Mechanic"
        __app_description__ = "Text Mechanic"
        __app_author__ = "Waqas"


a = Analysis(
    ['main.py'],
    pathex=[spec_dir],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'TextMechanic-{v.__version__}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.png'],
    company_name=v.__app_author__,
    product_name=v.__app_name__,
    file_description=v.__app_description__,
    legal_copyright=f"(c) {v.__app_author__}",
)
