include .env
export 

run-dev:
	uvicorn src.main:app --host $(HOST) --port $(PORT) --reload