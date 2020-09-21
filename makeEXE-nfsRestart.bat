d:
cd D:\dev\python3\EasyOM_for_JCPT

del *.spec
rd /s /q build 
rd /s /q dist

pyinstaller -F -c -i "easyOM.ico" "autoRestartNFS.py"

del *.spec
rd /s /q build

pause