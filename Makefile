.PHONY: venv install dep seed clear show

venv:
	virtualenv -p python3 venv/

install:
	python3 setup.py install

clean:
	rm -rf ${VIRTUAL_ENV}/lib/python3.6/site-packages/Platform_Importer.*.egg
	rm -rf build dist *.egg-info

dep:
	pip install -r requirements.txt
