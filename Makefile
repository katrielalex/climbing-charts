local-scrape: build
	sam local invoke ClimbingScraperFunction

local-show: build
	sam local invoke ClimbingDisplayFunction

local-serve: build
	sam local start-api

deploy: build
	sam deploy

build:
	sam build --use-container
