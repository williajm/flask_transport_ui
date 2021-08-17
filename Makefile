all: isort black flake

isort:
	isort transport tests

black:
	black transport tests

flake:
	flake8 transport tests
