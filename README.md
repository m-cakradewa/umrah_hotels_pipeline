# Umrah Hotels Data Pipeline
Automated data pipeline that collects Hotel availability and pricing data for Mecca from UmrahMe, processes the data through a medaillon architecture, and serves aggregated insights for dashboard analytics.<br><br>
The system helps visualize hotel price trends accross different time horizons and hotel star categories, helping travel planners to estimate accomodation costs for future umrah trips.
_____

# Problem
Hotel prices and availability in Makkah fluctuate significantly throughout the year, depending on a few aspects such as:
- seasonality (according to lunar calendar)
- demand 
- proximity to religious events
- booking horizon

Travel planners often lack a structured overview of price trends across time horizons.<br><br>
This project creates a pipeline that fetches and processes hotel data daily to real-time price insights.
_____

# Solution
An automated pipeline that
- scrapes hotel availability and pricing data
- stores raw data in Bronze layer
- cleans and structures data in Silver layer
- creates analytical views in Gold layer
- delivers insights as a dashboard
_____

# Tech Stack
| Component | Tool |
| ---------- | ---------- |
| Orchestration | dbt (Data Build Tool) |
| Transformation | PostgreSQL |
Containerization | Docker |
Dashboarding | Streamlit |
Scraping | Python |
