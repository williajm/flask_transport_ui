all: lint

lint:
	pylint --disable=W1203,C0103,E1101,W0621,E1135,E1136,E1137,E0202 transport/ tests/*.py
