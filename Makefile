IMAGE="choffmeister/ocrmypdf-server"

test: build
	docker run --rm -it -p 8080:8080 $(IMAGE):latest

publish: build
	docker push $(IMAGE):latest

build:
	docker build -t $(IMAGE):latest .