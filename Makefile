TEST_DIR =tests
COV=MBSE

ODIR=obj
LDIR =sim_libs

.PHONY: clean, experiment, pytest

# default
all: sim
	@echo "Make all"

# Show help
help:
	@awk -f make-help.awk Makefile

# run Simulator
sim:
	@echo "Run Simulation"
	@./main.py; read -p "Close:" module;

clean:
	@echo "Clean"

# run experiment 1
exp:
	@cd experiment; python bank_example.py

# run sim2
run:
	@./run.py


# run pytest
pytest:
	@pytest -cov=$(COV) tests
