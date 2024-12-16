resource "google_compute_subnetwork" "new_subnet" {
  name          = "new-subnet"
  region        = var.region
  network       = "default"
  ip_cidr_range = "10.64.0.0/20"  # Ensure this CIDR does not conflict

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.65.0.0/20"  # Pods range
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.66.0.0/20"  # Services range
  }

  lifecycle {
    ignore_changes = [ip_cidr_range, secondary_ip_range]
  }
}

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone
  network  = "default"
  subnetwork = google_compute_subnetwork.new_subnet.name
  deletion_protection = false

  # ip_allocation_policy [{
  #   use_ip_aliases = true  # Enable IP aliasing

  #   pod_range {
  #     name          = "pods"        # Pod range name
  #     ip_cidr_range = "10.65.0.0/20"  # CIDR block for Pods
  #   }

  #   service_range {
  #     name          = "services"    # Service range name
  #     ip_cidr_range = "10.66.0.0/20"  # CIDR block for Services
  #   }
  # }]

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 10  # Adjust disk size as needed
    disk_type    = "pd-standard"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  initial_node_count = 1
}

resource "google_container_node_pool" "primary_nodes" {
  cluster    = google_container_cluster.primary.name
  location   = var.zone
  node_count = 1

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 10  # Adjust disk size as needed
    disk_type    = "pd-standard"  # Use standard persistent disks instead of SSDs
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  # Ensure pod IPv4 CIDR block is set for the node pool
  # pod_ipv4_cidr_block = "10.65.0.0/20"  # Should match the "pods" range
}

# resource "google_compute_router" "nat_router" {
#   name    = "nat-router"
#   network = google_compute_network.default.name
#   region  = var.region
# }

# resource "google_compute_router_nat" "nat_config" {
#   name   = "nat-config"
#   router = google_compute_router.nat_router.name
#   region = var.region

#   nat_ip_allocate_option = "AUTO_ONLY"
#   source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
# }


