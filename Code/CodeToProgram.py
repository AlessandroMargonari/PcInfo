import PyInstaller.__main__

# Pass the script file as the first argument
PyInstaller.__main__.run([
    #file path
    'E:\Desktop\Projects\PCInfo\Code\systemInfoDesktop.pyw',
    '--name=System Info',
    '--noconfirm',
    '--onefile',
    '--console',
    '--windowed'
])