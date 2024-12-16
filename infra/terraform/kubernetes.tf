# Enable the Container Registry API
resource "google_project_service" "container_registry" {
  project = var.project_id
  service = "containerregistry.googleapis.com"
}

# (Optional) Create a Google Cloud Storage bucket for Container Registry
resource "google_storage_bucket" "gcr_bucket" {
  name          = "gcr-${var.project_id}"
  location      = "US"
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}

resource "kubernetes_service_account" "dms_kb_sa" {
  metadata {
    name      = "dms-kb-sa"
    namespace = "default"  # You can change this to another namespace if needed
  }
}

resource "kubernetes_cluster_role" "cluster_admin" {
  metadata {
    name = "dms-cluster-admin"
  }

  rule {
    api_groups = [""]
    resources  = ["pods", "services", "deployments", "replicasets", "endpoints"]
    verbs      = ["*"]
  }
}

resource "kubernetes_role" "edit_role" {
  metadata {
    name      = "edit"
    namespace = "default"
  }

  rule {
    api_groups = [""]
    resources  = ["pods", "services", "deployments", "replicasets"]
    verbs      = ["create", "get", "list", "update", "delete"]
  }
}

resource "kubernetes_cluster_role_binding" "my_cluster_admin_binding" {
  metadata {
    name = "my-cluster-admin-binding"
  }

  role_ref {
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.cluster_admin.metadata[0].name
    api_group = "rbac.authorization.k8s.io"
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.dms_kb_sa.metadata[0].name
    namespace = kubernetes_service_account.dms_kb_sa.metadata[0].namespace
  }
}

resource "kubernetes_secret" "db_credentials" {
  depends_on = [google_sql_database_instance.postgres_instance]
  metadata {
    name = "db-credentials"
  }

  data = {
    POSTGRES_HOST     = google_sql_database_instance.postgres_instance.connection_name
    POSTGRES_USER     = google_sql_user.default.name
    POSTGRES_PASSWORD = google_sql_user.default.password
    POSTGRES_DB       = google_sql_database.database.name
  }
}

# resource "kubernetes_service" "flask_app" {
#   metadata {
#     name = "dms-dev-service"
#   }

#   spec {
#     selector = {
#       app = "dms-dev"
#     }

#     port {
#       port        = 80
#       target_port = 5000
#     }

#     type = "LoadBalancer"
#   }

#   lifecycle {
#     ignore_changes = [
#       spec,
#       metadata
#     ]
#   }
  
#   depends_on = [google_container_cluster.primary]
# }

# resource "kubernetes_deployment" "flask_app" {
#   depends_on = [
#     kubernetes_service.flask_app         # Ensure the service is created first
#   ]

#   metadata {
#     name = "dms-dev"
#     labels = {
#       app = "dms-dev"
#     }
#   }

#   spec {
#     replicas = 1

#     selector {
#       match_labels = {
#         app = "dms-dev"
#       }
#     }

#     template {
#       metadata {
#         labels = {
#           app = "dms-dev"
#         }
#       }

#       spec {
#         container {
#           image = "gcr.io/${var.project_id}/dms-dev:latest"
#           name  = "dms-dev"
#           port {
#             container_port = 5000
#           }
#         }

#         image_pull_secrets {
#           name = "dms-gcr-secret"  # Reference the secret created earlier
#         }
#       }
#     }
#   }
# }

