output "repository_name" {
  description = "The name of the Artifact Registry repository"
  value       = google_artifact_registry_repository.my-repo.name
}
