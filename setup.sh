#!/bin/bash

# Check the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux OS"
    PKG_MANAGER="apt"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    PKG_MANAGER="brew"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Detected Windows"
    echo "Windows does not have a package manager for Python packages."
    echo "Please install the required packages using pip manually."
    exit 1
else
    echo "Unsupported operating system"
    exit 1
fi

# Install required Python packages if not already installed
for package in "numpy" "joblib" "matplotlib"; do
    if ! python3 -c "import $package" &> /dev/null; then
        echo "$package is not installed. Installing..."
        $PKG_MANAGER install -y python3-$package
        if [ $? -eq 0 ]; then
            echo "$package installed successfully."
        else
            echo "Failed to install $package."
            exit 1
        fi
    else
        echo "$package is already installed."
    fi
done

# Check if cv2 can be imported (special case for OpenCV)
if ! python3 -c "import cv2" &> /dev/null; then
    echo "cv2 is not installed. Please install it manually."
else
    echo "cv2 is already installed."
fi
