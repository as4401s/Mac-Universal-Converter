# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

datas = [('/Users/arjunsarkar/Mac-image-converter/.venv/lib/python3.12/site-packages/customtkinter', 'customtkinter')]
datas += copy_metadata('imageio')
datas += copy_metadata('imageio_ffmpeg')
datas += copy_metadata('moviepy')
datas += copy_metadata('proglog')
datas += copy_metadata('numpy')
datas += copy_metadata('Pillow')
datas += copy_metadata('pillow-heif')


a = Analysis(
    ['converter.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['pillow_heif', 'PIL._tkinter_finder', 'PIL._webp', 'moviepy', 'moviepy.editor', 'moviepy.video', 'moviepy.video.io', 'moviepy.video.fx', 'moviepy.video.fx.all', 'moviepy.audio', 'moviepy.audio.io', 'moviepy.audio.fx', 'moviepy.audio.fx.all', 'moviepy.config', 'moviepy.tools', 'proglog', 'decorator', 'imageio', 'imageio_ffmpeg', 'numpy', 'requests', 'tqdm', 'moviepy.video.tools', 'moviepy.audio.tools', 'moviepy.video.compositing', 'moviepy.audio.AudioClip', 'moviepy.video.VideoClip'],
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
    [],
    exclude_binaries=True,
    name='MacConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['AppIcon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MacConverter',
)
app = BUNDLE(
    coll,
    name='MacConverter.app',
    icon='AppIcon.icns',
    bundle_identifier='com.arjunsarkar.macconverter',
)
