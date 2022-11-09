TEST_DIR =tests
COV=MBSE

ODIR=obj
LDIR =sim_libs

.PHONY: clean, experiment, pytest

all:
	@echo "Make all"

clean:
	@echo "Clean"

exp:
	@cd experiment; python bank_example.py

pytest:
	@pytest -cov=$(COV) tests
