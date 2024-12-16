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


resource "kubernetes_service" "flask_app" {
  metadata {
    name = "dms-dev-service"
  }

  spec {
    selector = {
      app = "dms-dev"
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }

  lifecycle {
    ignore_changes = [
      spec,
      metadata
    ]
  }
  
  depends_on = [google_container_cluster.primary]
}

resource "kubernetes_deployment" "flask_app" {
  depends_on = [
    kubernetes_service.flask_app         # Ensure the service is created first
  ]

  metadata {
    name = "dms-dev"
    labels = {
      app = "dms-dev"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "dms-dev"
      }
    }

    template {
      metadata {
        labels = {
          app = "dms-dev"
        }
      }

      spec {
        container {
          image = "gcr.io/${var.project_id}/dms-dev:latest"
          name  = "dms-dev"
          image_pull_secrets = [{
            name = "gcr-secret"
          }]
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

