# -*- mode: python -*-

block_cipher = None


a = Analysis(['OCR_Labeler.py'],
             pathex=['E:\\pyProject\\SuperLabelTool_OCR'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='OCR_Labeler',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icons\\dragon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='OCR_Labeler')
