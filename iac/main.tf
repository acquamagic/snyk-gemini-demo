terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ------------------------------------------------------------
# ⚠️  Intentionally Insecure Bastion Host (for Snyk IaC demo)
# ------------------------------------------------------------

# Existing Service Account (no creation here)
data "google_service_account" "existing_sa" {
  account_id = var.service_account_id
}

resource "google_compute_network" "demo_network" {
  name                    = "demo-network"
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "allow_ssh_insecure" {
  name    = "allow-ssh-insecure"
  network = google_compute_network.demo_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  # ⚠️ Insecure: Allow SSH from anywhere (0.0.0.0/0)
  source_ranges = ["0.0.0.0/0"]

  target_tags = ["bastion"]
  description = "Insecure firewall rule allowing SSH from all IPs - for demo only"
}

resource "google_compute_instance" "bastion_host" {
  name         = "snyk-demo-bastion"
  machine_type = "e2-micro"
  zone         = var.zone

  tags = ["bastion"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = google_compute_network.demo_network.name
    access_config {} # Assigns a public IP
  }

  service_account {
    email  = data.google_service_account.existing_sa.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    ssh-keys = "demo-user:${file("~/.ssh/id_rsa.pub")}"
  }

}

output "bastion_ip" {
  description = "Public IP address of the insecure bastion host"
  value       = google_compute_instance.bastion_host.network_interface[0].access_config[0].nat_ip
}
