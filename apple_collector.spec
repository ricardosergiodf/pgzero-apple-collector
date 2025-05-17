# apple_collector.spec
import os
import pgzero

block_cipher = None

pgzero_data_path = os.path.join(os.path.dirname(pgzero.__file__), 'data')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('images/*.png', 'images'),
        ('sounds/*.wav', 'sounds'),
        ('music/*.mp3', 'music'),
        (pgzero_data_path + '/*.png', 'pgzero/data'),  # Copia os PNGs do pgzero/data, incluindo icon.png
    ],
    hiddenimports=['pgzrun'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AppleCollector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AppleCollector'
)
