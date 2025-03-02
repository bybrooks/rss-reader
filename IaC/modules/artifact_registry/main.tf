resource "google_artifact_registry_repository" "my-repo" {
  location      = var.registry_location
  repository_id = var.repository_id
  description   = "RSS Service Repository"
  format        = var.format
}
