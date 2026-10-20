# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

ROOT = Path(SPECPATH)
def tree(source, dest):
    source = ROOT / source
    result = []
    if source.exists():
        for p in source.rglob("*"):
            if p.is_file():
                result.append((str(p), str(Path(dest) / p.relative_to(source).parent)))
    return result

datas = []
datas += tree("qml", "qml")
datas += tree("assets", "assets")
datas += collect_data_files("certifi")
hiddenimports = ["certifi", "requests", "PySide6.QtQml", "PySide6.QtQuick"]
a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="VNDELAY",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=None,
    uac_admin=False,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, upx_exclude=[], name="VNDELAY")
