.PHONY: test model-check demo audit

test:
	PYTHONPATH=src python -m pytest -q

model-check:
	PYTHONPATH=src python formal/bounded_model_check.py

demo:
	PYTHONPATH=src python -m dikwp_sirr demo --output .sirr-demo

audit:
	python scripts_static_audit.py
