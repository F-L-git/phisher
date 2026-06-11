# PHISHER 🐠
Development of tools for identifying resources 
such as “Phishing” and “Shadow-IT”

██████╗░██╗░░██╗██╗░██████╗██╗░░██╗███████╗██████╗░
██╔══██╗██║░░██║██║██╔════╝██║░░██║██╔════╝██╔══██╗
██████╔╝███████║██║╚█████╗░███████║█████╗░░██████╔╝
██╔═══╝░██╔══██║██║░╚═══██╗██╔══██║██╔══╝░░██╔══██╗
██║░░░░░██║░░██║██║██████╔╝██║░░██║███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝

**Tool for detecting phishing resources and Shadow IT services in enterprise environments.**

## 📋 Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output Formats](#output-formats)
- [Examples](#examples)
- [License](#license)

## 🎯 Description

**FISHER** is a command-line utility for automated detection of:
- **Phishing domains and pages** — using signatures, trusted resource lists, SSL certificate analysis, and brand similarity checks.
- **Shadow IT** — unauthorized cloud services, SaaS applications, unregistered subdomains, and third-party tools used within the company.

This tool is useful for security analysts, SOC teams, and internal auditors.

## ✨ Features

- 🔍 Scan lists of URLs/domains for phishing indicators
- 🧩 Domain similarity checks (typosquatting, homograph attacks)
- ☁️ Detection of popular cloud services (Dropbox, Google Drive, Notion, Miro, etc.)
- 📡 Passive and active analysis of DNS records, whois, SSL certificates
- 📊 Export results to JSON, CSV, or SIEM-friendly formats
