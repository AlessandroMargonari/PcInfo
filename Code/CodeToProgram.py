import PyInstaller.__main__

# Pass the script file as the first argument
PyInstaller.__main__.run([
    #file path
    'E:\Desktop\Projects\PCInfo\Code\systemInfoDesktop.pyw',
    '--name=SystemInfo',
    '--icon=E:\Desktop\Projects\PCInfo\Other\icon.ico',
    '--noconfirm',
    '--onefile',
    '--console',
    '--windowed',
    '--clean'
])
