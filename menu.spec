# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['menu.py'],
             pathex=['D:\\Program Files (x86)\\проект игра pygame\\pygame-project'],
             binaries=[],
             datas=[('game.py', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Angkor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon='D:\\Program Files (x86)\\проект игра pygame\\pygame-project\\data\\image\\icon.ico', )
