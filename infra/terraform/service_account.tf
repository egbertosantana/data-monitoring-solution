# Create a Service Account
resource "google_service_account" "gcr_service_account" {
  account_id   = "dms-gcr-access-sa"
  display_name = "GCR Access Service Account"
}

# Create a Key for the Service Account
resource "google_service_account_key" "gcr_service_account_key" {
  service_account_id = google_service_account.gcr_service_account.id
}

# Export the key to use in Kubernetes (optional)
output "gcr_service_account_key_json" {
  value = google_service_account_key.gcr_service_account_key.private_key
  sensitive = true
}
