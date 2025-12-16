# Euprime_Assignment
Project Prototype Assignment under - Euprime


## Overview

This prototype demonstrates a **high-intent lead generation web agent** for the 3D in-vitro models space.  
The system simulates multi-source identification, enrichment, and probability-based ranking of potential leads.

It is designed to help business developers prioritize contacts most likely to engage with your product.

---

## Features

### 1. Identification
- Scans target profiles based on job titles like:
  - Director of Toxicology
  - Head of Preclinical Safety
  - VP Preclinical
- Data sources simulated in demo:
  - LinkedIn / Xing
  - PubMed / Google Scholar
  - Conference attendee lists (SOT, AACR)

### 2. Enrichment
- Adds contact info: email & phone
- Adds location info:
  - Distinguishes between personal location and company HQ

### 3. Ranking (Propensity to Buy Score)
- Scores leads (0–100) based on weighted signals:
  - Role Fit (Director/VP/Head) 
  - Publication recency (last 2 years) 
  - Conference presence 
  - Location in key hubs 
- Sorts table by highest probability first

### 4. Output
- Dynamic **Streamlit dashboard**
- Searchable table of leads
- Exportable to CSV
- Columns include:
  Name | Title | Company | Location | Email | Phone | Source | Score
  
---
## Screenshot of page : 
<img width="1919" height="938" alt="Image" src="https://github.com/user-attachments/assets/0acd532a-7bf0-4997-9b6c-f7f8ebf9baca" />

---
## Architecture

1. **Data Sources** (simulated)
 - LinkedIn / Xing
 - PubMed / bioRxiv
 - Conference websites (AACR, SOT)
 - Crunchbase / NIH grant data

2. **Pipeline**
Identification → Enrichment → Scoring → Display

3. **Extensible**
- Real APIs (Proxycurl, Hunter.io, Crunchbase) can replace placeholders
- Works with larger datasets

---

## Installation

```bash
# Install dependencies
pip install streamlit pandas biopython beautifulsoup4 requests
# Run the Streamlit app
streamlit run lead_pipeline_demo.py
```
Note: The demo currently uses manually seeded data.


