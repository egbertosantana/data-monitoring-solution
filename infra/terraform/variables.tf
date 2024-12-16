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

# variable "kubernetes_host" {}
# variable "client_certificate" {}
# variable "client_key" {}
# variable "cluster_ca_certificate" {}