SERVICE := home-assistant-health-checks
IMAGE := $(SERVICE)
SCRAP_IMAGE := scrap_$(SERVICE)
DATE := $(shell date --utc +%s)

export TIMESTAMP := $(DATE)

image:
	@docker build . -t $(IMAGE):latest -t $(IMAGE):$(TIMESTAMP)

run: image
	@docker run --rm --env-file .env --name home-assistant-health-checks $(IMAGE):$(TIMESTAMP)

shell: image
	@docker run -it --rm --env-file .env --name home-assistant-health-checks $(IMAGE):$(TIMESTAMP) bash