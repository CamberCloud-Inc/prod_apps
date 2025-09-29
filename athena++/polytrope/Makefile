# Makefile for Athena++ polytrope simulation
# This assumes Athena++ source is available

ATHENA_DIR = ../..
PROBLEM = polytrope
CONFIG_FLAGS = --prob=polytrope --coord=spherical_polar --gravity=fft

.PHONY: configure compile clean run plot

# Configure Athena++ for polytrope problem
configure:
	cd $(ATHENA_DIR) && python configure.py $(CONFIG_FLAGS)

# Compile Athena++
compile: configure
	cd $(ATHENA_DIR) && make clean && make -j4

# Generate initial conditions
ic:
	python3 polytrope_ic.py

# Clean build files
clean:
	cd $(ATHENA_DIR) && make clean

# Run simulation locally (for testing)
run: ic
	cd $(ATHENA_DIR) && ./athena -i ../polytrope/athinput.polytrope

# Plot results
plot:
	python3 plot_results.py

help:
	@echo "Available targets:"
	@echo "  configure - Configure Athena++ build"
	@echo "  compile   - Compile Athena++"
	@echo "  ic        - Generate initial conditions"
	@echo "  run       - Run simulation locally"
	@echo "  clean     - Clean build files"
	@echo "  plot      - Plot simulation results"