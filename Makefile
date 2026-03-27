.PHONY: build run clean inspect lint

IMAGE_NAME := youtube-transcript-mcp
CONTAINER_NAME := youtube-transcript-mcp-server
VENV := .venv

build:
	podman build -t $(IMAGE_NAME) .

run: build
	podman run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME)

run-dev: build
	podman run -it --rm -p 8000:8000 --entrypoint /bin/bash $(IMAGE_NAME)

stop:
	podman stop $(CONTAINER_NAME) || true

clean: stop
	podman rm $(CONTAINER_NAME) || true
	podman rmi $(IMAGE_NAME) || true

inspect:
	podman inspect $(IMAGE_NAME)

logs:
	podman logs -f $(CONTAINER_NAME)

$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install black

lint: $(VENV)
	$(VENV)/bin/black --check src/
