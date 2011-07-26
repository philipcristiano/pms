NOSETESTS = bin/nosetests -m '([Dd]escribe|[Ww]hen|[Ss]hould|[Tt]est)' -e DingusTestCase
PYTHON = PYTHONPATH=. bin/python

test:
	$(NOSETESTS) tests/*.py

clean:
	-rm -rf dist

develop:
	bin/python setup.py develop

.PHONY: dist
dist: clean
	bin/python setup.py sdist

virtualenv:
	virtualenv --no-site-packages --distribute .

requirements: virtualenv
	bin/easy_install -U distribute
	bin/pip install -r requirements.pip
	bin/easy_install nose_machineout

server:
	$(PYTHON) pms/app.py

deploy: create_plug
	bin/fab deploy

package_puppet:
	tar cfz puppet.tgz puppet

bootstrap: package_puppet, requirements
	vagrant up
	git submodule init
	git submodule update
	bin/fab bootstrap

create_plug: dist
	bin/plug create dist/pms-0.1.2.tar.gz

