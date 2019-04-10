all: lint

lint:
	pylint --disable=W1203,C0103,E1101 transport/ config/
