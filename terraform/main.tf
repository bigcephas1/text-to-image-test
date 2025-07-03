provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "docker_repo" {
  provider = google
  location = var.region
  repository_id = "text-to-image-repo"
  description   = "Docker repo for text-to-image PoC"
  format        = "DOCKER"
}

resource "google_cloud_run_service" "service" {
  name     = "text-to-image-service"
  location = var.region

  template {
    spec {
      containers {
        image = var.image_url
        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  location        = google_cloud_run_service.service.location
  project         = var.project_id
  service         = google_cloud_run_service.service.name
  role            = "roles/run.invoker"
  member          = "allUsers"
}

