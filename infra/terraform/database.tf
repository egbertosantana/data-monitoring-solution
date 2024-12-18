resource "google_sql_database_instance" "postgres_instance" {
  name             = "dms-postgres-instance"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = "db-f1-micro"  # Adjust tier as needed
    ip_configuration {
      psc_config {
        psc_enabled = true
        allowed_consumer_projects = [var.project_id]
      }
      ipv4_enabled = false
    }
    availability_type = "REGIONAL"
  }
}

resource "google_sql_database" "database" {
  name     = "dms-db"
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_sql_user" "default" {
  name     = "dms-admin"
  instance = google_sql_database_instance.postgres_instance.name
  password = "secret"
}

resource "google_sql_database_instance" "postgres_replica" {
  name             = "dms-postgres-replica-instance"
  database_version = "POSTGRES_13"
  region           = var.region

  master_instance_name = google_sql_database_instance.postgres_instance.name

  settings {
    tier = "db-f1-micro"  # Adjust tier as needed
    ip_configuration {
      psc_config {
        psc_enabled = true
        allowed_consumer_projects = [var.project_id]
      }
      ipv4_enabled = false
    }
    availability_type = "REGIONAL"
  }
}