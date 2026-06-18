# Hotel Revenue & Booking Intelligence (Project 4)

## Project Overview
This project analyses hotel booking data from 2015 to 2017, covering 119,389 bookings across City and Resort hotels. The goal was to uncover revenue loss patterns, cancellation drivers, and guest behaviour insights to support data-driven decisions in hotel operations and marketing strategy. Tools used: PostgreSQL, Python (Pandas, Matplotlib, Seaborn), and Power BI.

---

## Dataset
- **Source:** Hotel booking demand dataset
- **Table:** `hotel_cleaned` in PostgreSQL (`hotel_revenue` database)
- **Size:** 119,389 rows, 33 columns
- **Period:** 2015–2017 (2015 and 2017 are partial years)

---

## Data Cleaning
- Replaced NULL values in `children`, `agent`, and `company` columns with 0
- Removed 1 row with a negative ADR value
- Derived `total_revenue` column: `adr × (stays_in_weekend_nights + stays_in_week_nights)`
- Derived `quarter` column from `arrival_date_month` using `np.select()`
- Derived `period` column combining year and quarter (e.g. "2016 Q2")

---

## Exploratory Data Analysis
- Checked data types, null values, and distributions across all 33 columns
- Identified skewed ADR distribution and outliers
- Explored booking volume by hotel type, country, market segment, and time period
- Flagged 2015 and 2017 as partial years — excluded from YoY comparisons where relevant

---

## Business Questions Answered

| # | Question | Key Finding |
|---|----------|-------------|
| Q1 | Booking trends year-on-year | Peak bookings in Q2 (Apr–Jun) every year |
| Q2 | Cancellation rate by hotel type | City Hotel 41.73% vs Resort Hotel 27.76% |
| Q3 | Top countries by bookings | Portugal dominates with 48,590 bookings but 56.64% cancellation rate |
| Q4 | Repeated vs new guest behaviour | Repeated guests cancel less (14.49%) but pay lower ADR ($64 vs $103) |
| Q5 | Market segment analysis | Direct bookings: lowest cancellation (15.34%), highest ADR ($115). Groups: worst cancellation (61.07%) |

---

## Key Insights
- City Hotel loses **$10.88M** to cancellations — the single biggest revenue risk
- **Portugal** generates the most bookings but has a 56.64% cancellation rate — retention strategy needed
- **Q2 (April–June)** is peak booking season across all years — pricing and staffing should reflect this
- **Direct bookings** are the highest quality channel: low cancellation, high ADR
- **Group bookings** need strict deposit policies to reduce 61.07% cancellation rate
- **Repeated guests** are loyal but generate less revenue per booking — loyalty rewards should focus on upselling

---

## Visualisations
All charts saved in the `output/` folder:
- Chart 1: Cancellation Rate by Hotel Type (bar chart)
- Chart 2: Booking Trends by Quarter (line chart)
- Chart 3: Top 10 Countries by Confirmed Bookings (horizontal bar chart)
- Chart 4: Market Segment Analysis — Cancellation % vs Average ADR (clustered bar, twin axis)
- Chart 5: Repeated vs New Guest Comparison (side-by-side subplots)
- Power BI Dashboard: Hotel Performance Dashboard (2015–2017)

---

## Tools & Technologies
| Tool | Purpose |
|------|---------|
| PostgreSQL 18 | Data storage and SQL querying |
| Python (Pandas, NumPy) | Data cleaning, analysis, and EDA |
| Matplotlib / Seaborn | Data visualisation |
| Power BI (PL-300 certified) | Interactive dashboard |
| SQLAlchemy / psycopg2 | Python–PostgreSQL connection |
| Git / GitHub | Version control |

---

## Project Structure
```
hotel-revenue-project/
├── src/
│   ├── db.py          # SQLAlchemy database connection
│   ├── eda.py         # Exploratory data analysis
│   ├── cleaning.py    # Data cleaning steps
│   ├── analysis.py    # Business questions answered
│   └── visualise.py   # Charts and visualisations
├── output/            # Saved chart images
└── requirements.txt   # Python dependencies
```

---

## How to Run
1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate.bat
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL and restore the `hotel_revenue` database
5. Update database credentials in `src/db.py`
6. Run scripts in order: `cleaning.py` → `eda.py` → `analysis.py` → `visualise.py`

---

## Author
**Mahesh**
MSc Applied Data Science, University of Central Lancashire
PL-300 Power BI Certified