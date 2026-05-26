@echo off
chcp 65001 >nul
echo 正在检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python ^(https://www.python.org/downloads/^)
    echo 安装时请务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo 正在安装 PyInstaller...
python -m pip install pyinstaller

echo 正在打包番茄钟...
python -m PyInstaller --onefile --windowed --name "番茄钟" pomodoro.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [成功] 打包完成！
echo 可执行文件位于: dist\番茄钟.exe
echo.
pause
