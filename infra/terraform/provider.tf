terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"  # Use the latest stable version
    }
     kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"  # Use the latest stable version
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "kubernetes" {
  host                   = "https://${google_container_cluster.primary.endpoint}"
  token                  = "${data.google_client_config.default.access_token}"
  cluster_ca_certificate = "${base64decode(google_container_cluster.primary.master_auth.0.cluster_ca_certificate)}"
  client_key             = "${base64decode(google_container_cluster.primary.master_auth[0].client_key)}"
}