.PHONY: dependency-upgrade
dependency-upgrade:
	pip install pip-tools
	pip-compile --upgrade requirements.in
	pip-compile --upgrade requirements-devel.in
	pip-sync requirements.txt requirements-devel.txt
