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


## 🎯 Description

**FISHER** is a command-line utility for automated detection of:
- **Phishing domains and pages** — using signatures, trusted resource lists, SSL certificate analysis, and brand similarity checks.
- **Shadow IT** — unauthorized cloud services, SaaS applications, unregistered subdomains, and third-party tools used within the company.

The tool combines several methods: domain mutation generation, subdomain search by brand names, WHOIS data analysis, and image/keyword verification.

## ✨ Features

- **Generation and search of domain mutations** — uses dnstwist to create similar domains (typosquatting, homoglyphs, etc.) and verifies their existence through Netlas.
- **Subdomain search by brand** — searches for subdomains of the brandname type.* at level 3-4, excluding legitimate top domains.
- **WHOIS verification** — verifies registration data (organization, phone, email) with reference data.
- Double checking of suspicious domains:
  - **Detection of official images** (based on links from the perimeter)
  - **Search for keywords** (brand terms) on the page
  - **Criticality score** — each domain gets a rank from Legitimate (0) to High (3).
- A beautiful output to the console is a table with a color indication of danger (rich library).

> [!NOTE]
> **Note**: An active API key is required for the service. Netlas.io (registration is free, but there are limits on the number of requests)

## 🚀 Installation

### From source

```bash
#!/bin/bash
git clone https://github.com/your-org/fisher.git
cd fisher
pip install -r requirements.txt
python setup.py install
