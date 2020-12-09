# -*- mode: python -*-

block_cipher = None


a = Analysis(['hmark.py'],
             pathex=[r'C:\Users\Ivar_Svart\Documents\Dev\Hmark-4.0\Windows'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('icon.gif', r'C:\Users\Ivar_Svart\Documents\Dev\Hmark-4.0\Windows\icon.gif', 'DATA'), ('ctags.exe', r'C:\Users\Ivar_Svart\Documents\Dev\Hmark-4.0\Windows\ctags.exe', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='hmark_4.0.0_win_x64',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='icon.ico')