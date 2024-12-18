variable "project_id" {
  description = "Centrifugal Pump Data Monitoring Solution dev"
}

variable "region" {
  description = "region"
  default     = "southamerica-east1"
}

variable "zone" {
  description = "region"
  default     = "southamerica-east1-a"
}

variable "cluster_name" {
  description = "The name of the GKE cluster"
  default     = "dms-dev-app-cluster"
}