.PHONY: test unit_test perf_test coverage lint doc install clean

# Installation des dépendances
install:
	pip install -r requirements.txt
	pip install -r dev_requirements.txt

# Lance tous les tests
test:
	python -m pytest tests/

# Lance les tests unitaires et API (exclut performance)
unit_test:
	python -m pytest -k "not performance" tests/

# Lance uniquement les tests de performance
perf_test:
	python -m pytest -k "performance" tests/

# Rapport de couverture
coverage:
	coverage run -m pytest -k "not performance" tests/
	coverage report -m
	coverage html

# Vérification de la qualité du code (Linting)
lint:
	ruff check src/ tests/

# Génération de la documentation
doc:
	pdoc3 --html --output-dir docs src/

# Nettoyage
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf docs
	find . -type d -name "__pycache__" -exec rm -rf {} +