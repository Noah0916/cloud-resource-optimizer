variable "prefix" {
  type    = string
  default = "cloudopt"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "rg_name" {
  type    = string
  default = "rg-cloudopt"
}

variable "storage_account_name" {
  type = string
}

variable "acr_name" {
  type = string
}
