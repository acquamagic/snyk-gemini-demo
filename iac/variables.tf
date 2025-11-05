variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Region for resources"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Zone for bastion host"
  type        = string
  default     = "us-central1-a"
}

variable "service_account_id" {
  description = "Existing GCP service account ID (without domain, e.g., my-service-account)"
  type        = string
}
