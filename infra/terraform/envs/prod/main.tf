terraform {
  required_version = ">= 1.7.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }
}

# CLOUDFLARE_API_TOKEN from env, never in code. See ~/.ai/Common.md §4.
# Required token scopes:
#   - Account → Cloudflare Pages → Edit
#   - Zone → DNS → Edit (for the persona-atoms.com zone)
provider "cloudflare" {}

module "pages_project" {
  source = "git::https://github.com/convergent-systems-co/core-infra.git//terraform/cloudflare/pages-project?ref=v0.1.0"

  cloudflare_account_id = var.cloudflare_account_id
  project_name          = "persona-atoms"
  production_branch     = "main"
  custom_domain         = "persona-atoms.com"
  zone_id               = var.zone_id
}

variable "cloudflare_account_id" {
  description = "Cloudflare account ID that owns the Pages project."
  type        = string
}

variable "zone_id" {
  description = "Cloudflare zone ID for persona-atoms.com."
  type        = string
}

output "project_name" {
  value = module.pages_project.project_name
}

output "subdomain" {
  value       = module.pages_project.subdomain
  description = "Default *.pages.dev hostname for the project."
}

output "custom_domain" {
  value       = module.pages_project.custom_domain
  description = "Custom hostname attached to the Pages project."
}
