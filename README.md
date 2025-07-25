Banebooking is a booking system for sports sessions.

The docker image is pushed to Google Artifact Registry.

The service is deployed using Google Cloud Run by deploying a container image from the artifact registry.

By running `make deploy` the docker image is pushed to Google Artifact Registry and the service is deployed using Google Cloud Run.
