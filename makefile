include .env
export 

run-dev:
	uvicorn main:app --host $(HOST) --port $(PORT) --reload