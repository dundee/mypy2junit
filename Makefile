all: test

test:
	py.test tests

upload:
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

clean:
	rm -rf mypy2junit.egg-info build dist __pycache__

.PHONY: all test upload clean
