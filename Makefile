NOSETESTS = bin/nosetests -m '([Dd]escribe|[Ww]hen|[Ss]hould|[Tt]est)' -e DingusTestCase
PYTHON = PYTHONPATH=. bin/python

unit-test:
	$(NOSETESTS) tests/unit

test: unit-test

clean:
	-rm -rf dist

coverage:
	$(NOSETESTS) tests/unit --with-coverage --cover-tests --cover-package=pms
	rm .coverage

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

deploy: dist
	bin/fab deploy

package_puppet:
	git submodule init
	git submodule update
	tar cfz puppet.tgz puppet

.PHONY: puppet
puppet: package_puppet
	bin/fab bootstrap

bootstrap: package_puppet requirements
	vagrant up
	bin/fab bootstrap
