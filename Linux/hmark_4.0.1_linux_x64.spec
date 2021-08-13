# -*- mode: python -*-

block_cipher = None


a = Analysis(['hmark.py'],
             pathex=[r'/home/ibragim/Documents/Dev/Hmark-4.0/Linux'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('icon.gif', r'/home/ibragim/Documents/Dev/Hmark-4.0/Linux/icon.gif', 'DATA'), ('ctags', r'/home/ibragim/Documents/Dev/Hmark-4.0/Linux/ctags', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hmark_4.0.1_linux_x64',
          debug=False,
          strip=False,
          upx=True,
          console=True )
