run:
	poetry run python twitter_telegram.py

req:
	poetry export -f requirements.txt --output requirements.txt

build-docker:
	docker build -t twitter-telegram .

run-docker:
	docker run -t twitter-telegram