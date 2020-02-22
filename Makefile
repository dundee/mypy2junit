all: test

test:
	py.test tests

upload:
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

.PHONY: all test upload
