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

**PHISHER** is a command-line utility for automated detection of:
- **Phishing domains and pages** — using signatures, trusted resource lists, SSL certificate analysis, and brand similarity checks.
- **Shadow IT** — unauthorized cloud services, SaaS applications, unregistered subdomains, and third-party tools used within the company.
The tool combines several methods: domain mutation generation, subdomain search by brand names, WHOIS data analysis, and image/keyword verification.


## ✨ Features

- **Generation and search of domain mutations** — uses dnstwist to create similar domains (typosquatting, homoglyphs, etc.) and verifies their existence through `Netlas`.
- **`Subdomain` search by brand** — searches for subdomains of the `brandname.*` type at level 3-4, excluding legitimate top domains.
- **`WHOIS` verification** — verifies registration data (organization, phone, email) with reference data.
- **Double checking of suspicious domains**:
  - Detection of official images (based on links from the perimeter)
  - Search for keywords (brand terms) on the page
- **`Criticality score`** — each domain gets a rank from `Legitimate` (0) to `High` (3).
- A beautiful output to the console is a table with a color indication of danger (`rich` library).

> [!IMPORTANT]
> An active `API key` is required for the service `Netlas.io` (registration is free, but there are limits on the number of requests)

## 🔧 Setting up
### From source

Manual installation (`PIP` is recommended):
```bash
#!/bin/bash
    pip install netlas dnstwist beautifulsoup4 requests rich
```
> [!TIP]
> `dnstwist` may require the compilation of C extensions. If problems arise, install the dnstwist system package (for example, `sudo apt install dnstwist`), but the code uses the `dnstwist.run()` call, which the Python module expects. In this case, adaptation will be required.

## 📄 Preparation of the input JSON file (perimeter)
The tool accepts a JSON file with a description of the protected perimeter. An example is `perimeter_example.json`:

```json
  {
      "domains": ["pochtabank.ru", "pochtabank.phx.media"],
      "topdomains": ["pochtabank.ru", "phx.media", "nalogia.ru"],
      "brandnames": ["pochtabank", "pochta-bank", "postbank"],
      "whois": {
          "organisation": ["SC \"Post Bank\""]
      },
      "keywords": ["Почта Банк", "кредиты", "дебетовые", "карты", "вклады", "ипотека", "банк", "почта"],
      "imglinks": [
          "https://cdn.pochtabank.ru/_next/image?url=...background_2901_24.jpg"
      ]
  }
```

| Field | Type | Purpose |
|------------|---------------|----------------------------------------------------------------------------------------------|
| `domains` | list of rows | The organization's reference domains. Mutations (typos, substitutions) will be generated for them         |
| `topdomains` | list of strings | Valid "top" domains (for example, `pochtabank.ru` ). They are used to exclude legitimate subdomains during the search |
| `brandnames` | list of strings | Brand names (keywords for searching subdomains like `brandname.*`)                       |
| `whois` | object | Expected registration data. The organization key (a list of strings) is supported, as well as `phone` and `email` (present in the code, but not in the example) |
| `keywords` | list of strings | Words and phrases specific to the official website (will be searched on suspicious pages) |
| `imglinks` | list of strings | Absolute links to official images (for example, logos, banners). Their presence on the verified resource is checked |

## 🚀 Launching 

```bash
#!/bin/bash
  python __main__.py -p <perimeter.json> -a <NETLAS_API_KEY>
```
At startup, an ASCII banner, the version, the name of the team, and the progress of the steps are displayed.

## 📊 Interpretation of criticality
The `cout.print_domains()` table converts a numeric value to a text level:

| Number | Level | Value |
|-------|--------------|--------------------------------------------------------------------------------------------|
| 0 | `Legitimate` | Registration data matched the reference → trusted domain |
| 1 | `Low` | WHOIS didn't match, but there are no official images or keywords on the page |
| 2 | `Medium` | WHOIS mismatch + one additional feature (image or keyword)          |
| 3 | `High` | WHOIS mismatch + both signs (image + keywords) → high probability of phishing |

![output_example](src/phisher-console-output.png)

> **Note:** The `Critical` level (4) is not reached in the current implementation, but is reserved in the code.

## 🤝 License and authorship

The tool was developed by the **Knights of the Round Table** team. Version: `1.0.1#dev`.
The license is not specified in the source files, but it is intended to be used at the discretion of the authors (probably proprietary). When distributing, keep the title and the mention of authorship.

> [!CAUTION]
> 🐟 `Phisher` helps to detect digital threats and unauthorized resources in a timely manner. Use it as part of the perimeter monitoring process.
