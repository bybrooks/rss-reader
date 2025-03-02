variable "registry_location" {
  description = "The location of the Artifact Registry repository"
  default     = "asia-northeast1"
}

variable "repository_id" {
  description = "The ID of the Artifact Registry repository"
  default     = "rss-service-repo"
}

variable "format" {
  description = "The format of the Artifact Registry repository"
  default     = "DOCKER"
}
