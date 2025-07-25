PROJECT_ID        := banebooking
SERVICE_NAME      := banebooking
IMAGE_NAME        := gcr.io/$(PROJECT_ID)/$(SERVICE_NAME)
TAG               := latest
PLATFORM          := linux/amd64
REGION            := europe-north1
MEMORY            := 256Mi
TIMEOUT           := 1m

run:
	source .venv/bin/activate && python manage.py runserver

full-deploy:
	docker build --no-cache -t $(IMAGE_NAME):$(TAG) . --platform=$(PLATFORM)
	docker push $(IMAGE_NAME):$(TAG)
	gcloud run deploy $(SERVICE_NAME) \
	    --image $(IMAGE_NAME):$(TAG) \
	    --region $(REGION) \
	    --memory $(MEMORY) \
	    --timeout $(TIMEOUT) \
	    --project $(PROJECT_ID) \
	    --add-cloudsql-instances=banebooking:europe-west1:bwanebooking


build:
	docker build --no-cache -t $(IMAGE_NAME):$(TAG) . --platform=$(PLATFORM)

push:
	docker push $(IMAGE_NAME):$(TAG)

deploy:
	docker build --no-cache -t $(IMAGE_NAME):$(TAG) . --platform=$(PLATFORM)
	docker push $(IMAGE_NAME):$(TAG)
	gcloud run deploy $(SERVICE_NAME) \
	    --image $(IMAGE_NAME):$(TAG) \
	    --region $(REGION) \
	    --memory $(MEMORY) \
	    --timeout $(TIMEOUT) \
	    --project $(PROJECT_ID) \
	    --add-cloudsql-instances=banebooking:europe-west1:bwanebooking