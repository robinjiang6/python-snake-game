# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/badoo/Documents/GitHub/python-snake-game/snake.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/badoo/Documents/GitHub/python-snake-game/img', 'img/'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/sound', 'sound/'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/img/avogadro.png', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/img/bananabit.png', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/img/materwelon.ico', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/img/materwelon.png', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/img/strawberry.png', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/python_snake_game_model.py', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/python_snake_game_model_test.py', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/python_snake_game_shell.py', '.'), ('C:/Users/badoo/Documents/GitHub/python-snake-game/python_snake_game_view.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='snake',
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
    icon=['C:\\Users\\badoo\\Documents\\GitHub\\python-snake-game\\img\\materwelon.ico'],
)
