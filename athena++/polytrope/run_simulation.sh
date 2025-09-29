#!/bin/bash

# Script to run Athena++ polytrope simulation on Camber platform

echo "Setting up Athena++ polytrope star simulation..."

# Install dependencies
apt-get update
apt-get install -y build-essential python3 python3-pip git wget

# Install Python packages
pip3 install numpy scipy h5py matplotlib

# Download Athena++
if [ ! -d "athena" ]; then
    echo "Downloading Athena++..."
    git clone https://github.com/PrincetonUniversity/athena.git
fi

# Configure and compile Athena++
echo "Configuring and compiling Athena++..."
cd athena && ./configure.py --prob=blast --coord=spherical_polar --gravity=fft && make -j4 && cd ..

# Run simulation
echo "Starting polytrope simulation..."
./athena/bin/athena -i athinput.polytrope

echo "Simulation complete! Output files:"
ls -la polytrope*.hdf5 polytrope*.hst

# Create basic analysis plot if possible
if command -v python3 &> /dev/null; then
    echo "Creating analysis plots..."
    python3 << 'EOF'
import numpy as np
import h5py
import matplotlib.pyplot as plt

# Try to read the last output file
try:
    import glob
    files = sorted(glob.glob('polytrope*.hdf5'))
    if files:
        with h5py.File(files[-1], 'r') as f:
            print("Available datasets:", list(f.keys()))

        plt.figure(figsize=(12, 4))
        plt.suptitle('Polytrope Star Simulation Results')
        plt.tight_layout()
        plt.savefig('simulation_results.png', dpi=150, bbox_inches='tight')
        print("Results plot saved as simulation_results.png")
    else:
        print("No output files found to analyze")
except Exception as e:
    print(f"Analysis failed: {e}")
EOF
fi

echo "Simulation and analysis complete!"