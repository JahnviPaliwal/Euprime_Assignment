

import requests
from bs4 import BeautifulSoup
from Bio import Entrez
import re
import pandas as pd
import streamlit as st
from datetime import datetime
from manual_lead import *

Entrez.email = "email@example.com"
HUNTER_API_KEY = "hunter_api_key"


def scrape_social_networks(job_titles):
    # Placeholder for LinkedIn/Proxycurl/Xing
    # leads = []
    # headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
    #
    # for title in job_titles:
    #     params = {
    #         "query": title,
    #         "location": location_filter,
    #         "limit": 10
    #     }
    #
    #     response = requests.get(
    #         "https://nubela.co/proxycurl/api/v2/linkedin/search/people",
    #         headers=headers,
    #         params=params
    #     )
    #
    #     if response.status_code != 200:
    #         continue
    #
    #     for profile in response.json().get("results", []):
    #         leads.append({
    #             "name": profile.get("full_name"),
    #             "title": profile.get("occupation"),
    #             "company": profile.get("company"),
    #             "location": profile.get("location"),
    #             "email": None,
    #             "phone": None,
    #             "source": "linkedin",
    #             "tenure_months": profile.get("tenure_months", 0)
    #         })
    #
    # return leads

    # Normally fetch real profiles; here, I simulate

    leads = []

    leads += manual_social_network_leads()

    return leads



def scrape_publications(publication_keywords, job_titles, max_results=20):
    leads = []
    query = " AND ".join(publication_keywords)
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    if record["IdList"]:
        fetch = Entrez.efetch(
            db="pubmed",
            id=",".join(record["IdList"]),
            rettype="medline",
            retmode="text",
        )
        articles = fetch.read().split("\n\n")
        for article in articles:
            author = re.search(r"AU  - (.+)", article)
            title = re.search(r"TI  - (.+)", article)
            affiliation = re.search(r"AD  - (.+)", article)
            pub_date = re.search(r"DP  - (\d{4})", article)
            if author and title:
                aff_text = affiliation.group(1) if affiliation else ""
                location_match = re.search(
                    r",\s*([^,]+,\s*[A-Z]{2}|[^,]+,\s*[^,]+)$", aff_text
                )
                location = location_match.group(1) if location_match else ""
                if any(jt.lower() in aff_text.lower() for jt in job_titles):
                    recency_score = 0
                    if pub_date:
                        year = int(pub_date.group(1))
                        if datetime.now().year - year <= 2:
                            recency_score = 10
                    leads.append(
                        {
                            "name": author.group(1),
                            "title": next(
                                (
                                    jt
                                    for jt in job_titles
                                    if jt.lower() in aff_text.lower()
                                ),
                                "Researcher",
                            ),
                            "company": aff_text,
                            "location": location,
                            "email": None,
                            "phone": None,
                            "source": "pubmed",
                            "publication": title.group(1),
                            "recency_score": recency_score,
                        }
                    )
    return leads


def scrape_conferences(conference_urls, job_titles):
    # leads = []
    #
    # for url in conference_urls:
    #     response = requests.get(url, timeout=10)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #
    #     speakers = soup.find_all(["div", "li"], class_=re.compile("speaker|author|presenter", re.I))
    #
    #     for sp in speakers:
    #         text = sp.get_text(" ", strip=True)
    #
    #         leads.append({
    #             "name": text.split(",")[0],
    #             "title": text,
    #             "company": "",
    #             "location": "",
    #             "email": None,
    #             "phone": None,
    #             "source": "conference",
    #             "publication": soup.title.text if soup.title else "Conference Speaker"
    #         })
    #
    # return leads


    leads = []
    for url in conference_urls:
        leads += manual_publication_leads()
    return leads


def enrich_budget_info(leads):
    # Placeholder: Normally fetch from Crunchbase, NIH
    for lead in leads:
        if "Pfizer" in lead.get("company", ""):
            lead["funding_score"] = 20
        else:
            lead["funding_score"] = 10
    return leads



def enrich_contacts(leads):
    # for lead in leads:
    #     company = lead.get("company")
    #     if not company:
    #         continue
    #
    #     domain = company.replace(" ", "").lower() + ".com"
    #     url = f"https://api.hunter.io/v2/domain-search"
    #     params = {
    #         "domain": domain,
    #         "api_key": HUNTER_API_KEY
    #     }
    #
    #     r = requests.get(url, params=params)
    #     if r.status_code == 200:
    #         emails = r.json().get("data", {}).get("emails", [])
    #         if emails:
    #             lead["email"] = emails[0]["value"]
    #
    # return leads
    for lead in leads:
        if lead.get("company"):
            # Placeholder: Normally call Hunter.io
            lead["email"] = (
                f"{lead['name'].split()[0].lower()}@{lead['company'].split()[0].lower()}.com"
            )
            # lead["phone"] = "555-123-4567"
    return leads


def rank_leads(leads):
    for lead in leads:
        score = 0

        if lead["title"]:
            if "director" in lead["title"].lower():
                score += 30
            elif "vp" in lead["title"].lower():
                score += 25
            elif "head" in lead["title"].lower():
                score += 20
        # Email available
        if lead.get("email"):
            score += 25
        # Publication
        if lead.get("source") == "pubmed":
            score += 25
        # Recency from publication
        score += lead.get("recency_score", 0)
        # Conference presence
        if lead.get("source") == "conference":
            score += 15
        # Funding/Grant
        score += lead.get("funding_score", 0)
        # Location known
        if lead.get("location"):
            score += 10
        lead["score"] = score
    return sorted(leads, key=lambda x: x["score"], reverse=True)



#Sreamlit Dashboard

def display_scoreboard(leads):
    st.set_page_config(layout="wide")
    st.title("High-Intent Lead Scoreboard")
    df = pd.DataFrame(leads)
    df = df[
        ["name", "title", "company", "location", "email", "phone", "source", "score"]
    ].sort_values("score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download CSV", df.to_csv(index=False), "lead_scoreboard.csv", "text/csv"
    )


def run_pipeline():
    job_titles = ["Director", "VP", "Head"]
    publication_keywords = [
        "Drug-Induced Liver Injury",
        "Organ-on-chip",
        "Hepatic spheroids",
    ]
    conference_urls = ["https://conference.org/speakers"]

    leads = []
    leads += scrape_social_networks(job_titles)
    leads += scrape_publications(publication_keywords, job_titles)
    leads += scrape_conferences(conference_urls, job_titles)
    leads = enrich_budget_info(leads)
    leads = enrich_contacts(leads)
    leads = rank_leads(leads)
    return leads


ranked_leads = run_pipeline()
display_scoreboard(ranked_leads)

