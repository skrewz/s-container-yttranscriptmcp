.PHONY: build run clean inspect lint

IMAGE_NAME := yt-transcript-mcp
CONTAINER_NAME := yt-transcript-mcp-server
YTTRANSCRIPTMCP_PORT ?= 9042

build:
	podman build --no-cache -t $(IMAGE_NAME) .

run: build
	podman run --replace --rm --name $(CONTAINER_NAME) -p $(YTTRANSCRIPTMCP_PORT):$(YTTRANSCRIPTMCP_PORT) -e YTTRANSCRIPTMCP_PORT=$(YTTRANSCRIPTMCP_PORT) $(IMAGE_NAME)

stop:
	podman stop $(CONTAINER_NAME) || true

clean: stop
	podman rm $(CONTAINER_NAME) || true
	podman rmi $(IMAGE_NAME) || true

inspect:
	podman inspect $(IMAGE_NAME)

logs:
	podman logs -f $(CONTAINER_NAME)

lint:
	uv run --with black black --check src/

test:
	curl -v "http://localhost:$(YTTRANSCRIPTMCP_PORT)/mcp" \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
		|| echo "Server not running. Run 'make run' first."
