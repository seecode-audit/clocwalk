SRC_DIR = clocwalk
MAKE = make
PY_VERSION=`python -c "import sys; v = sys.version_info; sys.stdout.write('py%d%d' % (v[0], v[1]))"`

.PHONY: clean test lint intsall sdist

all:
	make install
	make test
	make clean

install:
	pip install .[dev,test,docs]

unit:
	export PYTHONPATH=$(SRC_DIR) && nosetests -x -v --nocapture \
	--with-coverage --cover-erase --cover-package=$(SRC_DIR) \
	tests/unit/

clean:
	rm -rf *.egg
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf man
	rm -rf $(SRC_DIR)/*.egg-info
	find $(SRC_DIR) tests -name '*.pyc' | xargs rm -rf
