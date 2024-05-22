venv/run:
	. ./venv/bin/activate

venv/stop:
	deactivate

server/run:
	uvicorn main:app --reload

.PHONY: venv/run, venv/stop
