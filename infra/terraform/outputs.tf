output "cluster_name" {
  value = google_container_cluster.primary.name
}

# Outputs
output "cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth.0.cluster_ca_certificate
  sensitive = true
  description = "CA certificate for the cluster"
}

output "client_certificate" {
  value = google_container_cluster.primary.master_auth.0.client_certificate
  sensitive = true
  description = "Client certificate for the cluster"
}

output "client_key" {
  value = google_container_cluster.primary.master_auth.0.client_key
  sensitive = true
  description = "Client key for the cluster"
}

output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
  description = "Kubernetes API server endpoint"
}