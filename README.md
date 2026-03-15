# Umrah Hotels Data Pipeline
Automated data pipeline that collects Hotel availability and pricing data for Mecca from UmrahMe, processes the data through a medaillon architecture, and serves aggregated insights for dashboard analytics.<br><br>
The system helps visualize hotel price trends accross different time horizons and hotel star categories, helping travel planners to estimate accomodation costs for future umrah trips.

---

# Problem
Hotel prices and availability in Makkah fluctuate significantly throughout the year, depending on a few aspects such as:
- seasonality (according to lunar calendar)
- demand 
- proximity to religious events
- booking horizon

Travel planners often lack a structured overview of price trends across time horizons.<br><br>
This project creates a pipeline that fetches and processes hotel data daily to real-time price insights.

---

# Solution
An automated pipeline that
- scrapes hotel availability and pricing data
- stores raw data in Bronze layer
- cleans and structures data in Silver layer
- creates analytical views in Gold layer
- delivers insights as a dashboard
---

# Tech Stack
| Component | Tool |
| ---------- | ---------- |
| Orchestration | dbt (Data Build Tool) |
| Transformation | PostgreSQL |
Containerization | Docker |
Dashboarding | Streamlit |
Scraping | Python |

---

# Architecture Diagram

                +----------------------+
                |  UmrahMe Website     |
                +----------+-----------+
                           |
                           | scraping
                           ▼
                    +-------------+
                    | Python      |
                    | Scraper     |
                    +------+------+ 
                           |
                           ▼
                    +-------------+
                    | PostgreSQL  |
                    | Bronze      |
                    +------+------+ 
                           |
                           | dbt transformation
                           ▼
                    +-------------+
                    | Silver      |
                    | Clean Data  |
                    +------+------+ 
                           |
                           | dbt aggregation
                           ▼
                    +-------------+
                    | Gold Views  |
                    +------+------+ 
                           |
                           ▼
                    +-------------+
                    | Streamlit   |
                    | Dashboard   |
                    +-------------+
---

# Airflow DAG
Pipeline orchestration using Airflow.

                    +-------------+
                    |    Start    |
                    +------+------+
                           |
                           ▼
                    +---------------+
                    | scrape_data   |
                    |   (python)    |
                    +------+--------+
                           |
                           ▼
                    +--------------+
                    | store_bronze |
                    | PostgreSQL   |
                    +------+-------+
                           |
                           ▼
                    +---------------+
                    | run_dbt       |
                    | create_silver |
                    +------+--------+
                           |
                           ▼
                    +-------------+
                    | run_dbt     |
                    | create_gold |
                    +------+------+
                           |
                           ▼
                    +-----------------+
                    | build Streamlit |
                    |     Webapp      |
                    +------+----------+
                           |
                           ▼
                    +-------------+
                    |     End     |
                    +-------------+
---

# Data Collection Strategy
The scraper collects hotel data (stars, price per night, location, available date) across multiple time horizons for check-in date.
### Within a week
- 3 days
- 4 days
- 5 days
- 6 days

### Within a month
- 1 week
- 2 weeks
- 3 weeks
- 4 weeks

### Monthly horizon
- 1 month
- 2 months
- 3 months
- 4 months

### Long-term trend
- monthly snapshots for the upcoming 12 months

---

# Data Layers
### Bronze
- raw scraped data
- newly scraped saved in the same table as new rows
### Silver
- cleaned, transformed, and standardized
- ready to be aggregated
### Gold
- aggregated views for analytics
- can either be tables, views, or mix of both
- metrics: average hotel price, average number of available hotels
- grouping: stars, time horizon, distance to holy mosque

---

# Dashboard Concept
The dashboard visualizes hotel pricing using a grid layout.
| Time horizon | 2 stars | 3 stars | 4 stars | 5 stars |
|--------------|---------|---------|---------|---------|
| Within 1W    |         |         |         |         |
| Within 1 Mo  |         |         |         |         |
| Within 4 Mos |         |         |         |         |
<br>
### Purposes
- help travelers estimate budget requirements
- compare near-term vs future travel
- visualize hotel availability trends

---

# Running the Pipeline
To start:
> docker compose up --build

Airflow sequence of tasks include:
1. scraping job
2. data storage
3. dbt transformation(s)

