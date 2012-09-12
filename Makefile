.SILENT:

clean:
	find . -iname '*.pyc' -exec rm -f {} \;

test: clean
	nosetests -s tests
