HEROKU_APP_NAME=shifts-api
COMMIT_ID=$(shell git rev-parse HEAD)

heroku-login:
	HEROKU_API_KEY=${HEROKU_API_KEY} heroku auth:token

heroku-container-login:
	HEROKU_API_KEY=${HEROKU_API_KEY} heroku container:login

build-app-heroku: heroku-container-login
	docker buildx build --platform linux/amd64 -t registry.heroku.com/$(HEROKU_APP_NAME)/web ./src

push-app-heroku: heroku-container-login
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web

release-heroku: heroku-container-login
	heroku container:release web --app $(HEROKU_APP_NAME)

.PHONY: heroku-login heroku-container-login build-app-heroku push-app-heroku
