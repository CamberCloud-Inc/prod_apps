#!/bin/bash
# Usage: ./run_sim.sh <left_force_duration>
if [ $# -ne 1 ]; then
    echo "Usage: $0 <left_force_duration>"
    echo "Example: $0 20000"
    exit 1
fi

LEFT_FORCE_DURATION=${1:-20000}  # Use default value if not provided
# Fixed velocity values for consistent simulation
BREAK_VELOCITY=0.003

# Function to find Python 3 binary
find_python3() {
    for cmd in python3 python3.9 python3.10 python3.11 python3.12 python; do
        if command -v "$cmd" >/dev/null 2>&1; then
            # Check if it's Python 3
            if "$cmd" -c "import sys; exit(0 if sys.version_info[0] == 3 else 1)" 2>/dev/null; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    echo "Error: Python 3 not found!" >&2
    exit 1
}

# Get Python 3 binary
PYTHON_BIN=$(find_python3)
echo "Using Python: $PYTHON_BIN"

# Install Python requirements if they don't exist
echo "Checking Python dependencies..."
if ! $PYTHON_BIN -c "import MDAnalysis" 2>/dev/null; then
    echo "Installing Python requirements..."
    
    # Try different methods to install packages
    if $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
        # pip module is available
        $PYTHON_BIN -m pip install --user --no-warn-script-location -r requirements.txt
    elif command -v pip3 >/dev/null 2>&1; then
        # pip3 command is available
        pip3 install --user --no-warn-script-location -r requirements.txt
    elif command -v pip >/dev/null 2>&1; then
        # pip command is available
        pip install --user --no-warn-script-location -r requirements.txt
    else
        # Try to install pip first
        echo "pip not found. Trying to install pip..."
        if command -v apt-get >/dev/null 2>&1; then
            # Debian/Ubuntu systems
            echo "Please run: sudo apt-get update && sudo apt-get install python3-pip"
        elif command -v yum >/dev/null 2>&1; then
            # RHEL/CentOS systems
            echo "Please run: sudo yum install python3-pip"
        elif command -v dnf >/dev/null 2>&1; then
            # Fedora systems
            echo "Please run: sudo dnf install python3-pip"
        else
            echo "Please install pip for Python 3 manually"
        fi
        echo "Error: No pip installation method available!" >&2
        exit 1
    fi
    
    # Check if installation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Python requirements!" >&2
        echo "You may need to install packages manually or with system package manager:" >&2
        echo "  - python3-numpy" >&2
        echo "  - python3-matplotlib" >&2
        echo "  - python3-pandas" >&2
        exit 1
    fi
fi

# Add user's local bin to PATH if it exists
if [ -d "$HOME/.local/bin" ]; then
    case ":$PATH:" in
        *":$HOME/.local/bin:"*) ;;
        *) export PATH="$HOME/.local/bin:$PATH" ;;
    esac
fi

# Also add Python user site-packages to PYTHONPATH
USER_SITE_PACKAGES=$($PYTHON_BIN -m site --user-site 2>/dev/null)
if [ -n "$USER_SITE_PACKAGES" ] && [ -d "$USER_SITE_PACKAGES" ]; then
    export PYTHONPATH="$USER_SITE_PACKAGES:$PYTHONPATH"
fi

# Run LAMMPS simulation in parallel with LEFT_FORCE_DURATION parameter
mpirun -np 4 lmp -in unbreakable.lmp -var LEFT_FORCE_DURATION $LEFT_FORCE_DURATION

# Run visualization with correct arrow duration
$PYTHON_BIN vis_stop.py --left_force_duration $LEFT_FORCE_DURATION --left_velocity $BREAK_VELOCITY

NPROCS=$(nproc)
