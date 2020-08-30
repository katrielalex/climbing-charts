local-scrape: build
	sam local invoke ClimbingScraperFunction

local-show: build
	sam local invoke ClimbingDisplayFunction

deploy: build
	sam deploy

build:
	sam build --use-container
