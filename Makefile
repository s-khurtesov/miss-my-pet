PATH_PYTHON=/usr/bin/python3
PATH_VENV_DIR=./venv
PATH_VENV_PYTHON=$(PATH_VENV_DIR)/bin/python3
PATH_REQUIREMENTS=./requirements.txt
PATH_PROJECT_DIR=./mysite

all: venv-check deps-python

clean: venv-clean

venv-create: venv-clean
	$(PATH_PYTHON) -m venv $(PATH_VENV_DIR)

venv-clean:
	rm -rf $(PATH_VENV_DIR)

PATH_CUR_ENV=$(shell python3 -m pip -V | awk '{print $$4}')
PATH_CUR_PYTHON=$(shell which python3)
venv-check:
	@test -d $(PATH_VENV_DIR) || (echo "ERROR: Run command \"make venv-create\" to create virtual environment" ; false)
	@test "$(PATH_CUR_ENV)" -ef "$(PATH_VENV_DIR)/lib/python3.6/site-packages" && \
		test "$(PATH_CUR_PYTHON) -ef $(PATH_VENV_PYTHON)" || \
		(echo "ERROR: Run command \"source $(PATH_VENV_DIR)/bin/activate\" to activate virtual environment" ; false)

venv-path:
	@echo "$(PATH_VENV_DIR)"

deps-python: venv-check
	python -m pip install -r $(PATH_REQUIREMENTS)
