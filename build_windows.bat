@echo off

setlocal

echo Checking for PyInstaller and PyQt5...
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller is not installed. Please install it with 'pip install pyinstaller'.
    exit /b 1
)

python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyQt5 is not installed. Please install it with 'pip install PyQt5'.
    exit /b 1
)

echo Ensure you have the right dependencies installed.
echo Press Enter to proceed with the build...
pause

set script_name=main.py
set output_dir=dist
if not exist "%output_dir%" (
    mkdir "%output_dir%"
)

echo Building the application...
pyinstaller --windowed --onefile "%script_name%" --distpath "%output_dir%" --hidden-import PyQt5

if %errorlevel% equ 0 (
    echo Build completed successfully! The executable is located in the '%output_dir%' folder.
) else (
    echo Build failed. Please check the output for errors.
)

if not exist "%script_name%" (
    echo The file '%script_name%' does not exist. Please ensure it is in the current directory.
    exit /b 1
)

exit /b

