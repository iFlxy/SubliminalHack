#!/bin/bash

check_dependencies() {
    echo "Checking for PyInstaller and PyQt5..."
    if ! command -v pyinstaller &> /dev/null; then
        echo "PyInstaller is not installed. Please install it with 'pip install pyinstaller'."
        exit 1
    fi

    if ! python3 -c "import PyQt5" &> /dev/null; then
        echo "PyQt5 is not installed. Please install it with 'pip install PyQt5'."
        exit 1
    fi
}

build_application() {
    local script_name="main.py"
    local output_dir="dist"
    mkdir -p "$output_dir"

    echo "Building the application..."
    pyinstaller --windowed --onefile "$script_name" --distpath "$output_dir" --hidden-import PyQt5

    if [[ $? -eq 0 ]]; then
        echo "Build completed successfully! The executable is located in the '$output_dir' folder."
    else
        echo "Build failed. Please check the output for errors."
    fi
}

main() {
    check_dependencies

    if [[ ! -f "main.py" ]]; then
        echo "The file 'main.py' does not exist. Please ensure it is in the current directory."
        exit 1
    fi

    echo "Ensure you have the right dependencies installed."
    echo "Press Enter to proceed with the build..."
    read -r

    build_application
}

main

