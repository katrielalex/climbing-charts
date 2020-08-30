local: build
	sam local invoke

build:
	sam build --use-container

deploy: build
	sam deploy
