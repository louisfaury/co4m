install:
		pip install --upgrade pip
		pip install -r requirements.txt
		python3 -m pip install -e "."

install-dev:
		pip install --upgrade pip
		pip install -r requirements.txt
		pip install -r test-requirements.txt
		python3 -m pip install -e "."

black:
		python3 -m black -l 100 co4m/

lint:
		python3 -m pylint -j 0 co4m/

test:
		python3 -m pytest tests/