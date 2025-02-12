# saas-scraper
SaaS Attribute Scraper

Overview

The SaaS Attribute Scraper is a Python-based tool that automates the process of extracting AI application identifiers and comprehensive application attributes for a growing set of AI apps and websites. The scraper leverages Selenium, Requests, and DNS lookups to gather high-quality characteristics with confidence.

Features

AI Application Identification – Automatically identifies AI-related applications.

Comprehensive Attribute Extraction – Captures vendor details, compliance information, security attributes, IAM (Identity & Access Management) support, GenAI features, and network security metrics.

Security & Compliance Checks – Analyzes security headers, TLS versions, and compliance certifications (GDPR, HIPAA, SOC 2, PCI DSS, FedRAMP, etc.).

Email & Domain Security Analysis – Retrieves SPF, DMARC, and DKIM records for spoofing risk assessment.

Automated Data Processing – Stores extracted attributes in structured CSV and JSON formats.

Workflow

1️⃣ Web Scraping (Selenium) – Extracting On-Page Data

Loads the target website using Selenium.

Extracts metadata like app name, vendor name, LinkedIn profile, and service type.

Searches the page source for compliance indicators (GDPR, HIPAA, etc.).

2️⃣ Security Headers Extraction (Requests)

Sends an HTTP HEAD request to the website.

Extracts key security headers like HSTS, X-Frame-Options, and Content-Security-Policy.

3️⃣ Compliance & Certifications (Keyword Matching in HTML Source)

Scans the page content for predefined compliance-related keywords.

Flags security certifications such as GDPR, HIPAA, SOC 2, and PCI DSS.

4️⃣ Email & Domain Security (DNS Lookups)

Performs SPF, DMARC, and DKIM record lookups.

Assesses email spoofing risk based on missing security records.

5️⃣ AI-Specific Features Extraction

Detects AI-specific attributes like data usage for model training, API availability, and AI-powered functionalities.

Scans for GenAI service offerings and enterprise plans.

6️⃣ Data Storage & Reporting

Saves extracted data into CSV and JSON files.

Provides confidence scoring for extracted attributes.

Installation

Prerequisites

Python 3.7+

Google Chrome & ChromeDriver (Ensure ChromeDriver is installed and compatible with your Chrome version)

Required Python Packages:

pip install selenium fake-useragent pandas requests dnspython

Usage

Running the Scraper

python script.py

The script will extract attributes from a predefined list of AI websites.

Results will be stored in ai_saas_attributes.csv and ai_saas_attributes.json.

Output

CSV Format:

app_name,vendor_name,gdpr,hipaa,soc2,iso27001,encryption_in_transit,spoof_risk_level
OpenAI,OpenAI Inc,True,False,True,False,TLS 1.2,Safe
Anthropic,Anthropic PBC,False,False,False,True,TLS 1.3,Critical

JSON Format:

[
  {
    "app_name": "OpenAI",
    "vendor_name": "OpenAI Inc",
    "gdpr": true,
    "hipaa": false,
    "soc2": true,
    "iso27001": false,
    "encryption_in_transit": "TLS 1.2",
    "spoof_risk_level": "Safe"
  }
]

Future Enhancements

Improved AI Feature Detection – Enhance scanning for LLM integrations and GenAI tools.

Proxy Support – Avoid bot detection with rotating IP proxies.

Deep Compliance Verification – Automate searches for privacy policies and terms of service.

License

This project is open-source and available under the MIT License.