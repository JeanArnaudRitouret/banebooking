# Banebooking

Banebooking is a web application for automatically booking sports sessions. It can handle checking availability, booking sessions including payment, and cancelling sessions. It also includes a calendar view of the bookings.

## Installation
Banebooking is a monorepo architecture using Django. It can be run locally or deployed to Google Cloud Platform.

### Local Installation


### Google Cloud Platform
The installation requires a Google Cloud Platform project with the following services enabled:
- Cloud Run
- Cloud SQL
- Cloud Storage
- Cloud Functions
- Cloud Scheduler

The infrastructure is deployed using Terraform.

The docker image is pushed to Google Artifact Registry.

The service is deployed using Google Cloud Run by deploying a container image from the artifact registry.

By running `make deploy` the docker image is pushed to Google Artifact Registry and the service is deployed using Google Cloud Run.


## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome.