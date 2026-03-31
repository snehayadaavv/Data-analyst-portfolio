## Data Analytics Portfolio – Sneha

Welcome to my **data analytics portfolio**. This repository highlights my end‑to‑end analytics skills across business understanding, data preparation, analysis, and insight communication.

- **Core skills**: SQL, Python, Power BI, Excel, statistics, experimentation, storytelling with data  
- **Focus areas**: product analytics, business intelligence, operations and customer analytics  
- **Strengths**: translating ambiguous business questions into analytical plans, building clear dashboards, and recommending actions that move metrics.

---

## 1. Signature Projects

Each project directory contains: a short problem brief, cleaned data (or data dictionary), notebooks/SQL, and an insight summary.

- **Customer Churn Diagnosis (`projects/customer-churn`)**  
  - Goal: Identify why customers leave and which levers best reduce churn.  
  - Stack: SQL for cohort and retention tables, Python (pandas, scikit‑learn) for feature analysis, Power BI for the executive dashboard.  
  - Deliverables: churn driver ranking, high‑risk segments, and a playbook of retention experiments.

- **Sales & Revenue Performance (`projects/sales-performance`)**  
  - Goal: Help leadership understand revenue trends by region, product, and channel.  
  - Stack: Excel for quick exploration, Power BI for interactive drill‑downs, DAX for advanced measures (e.g., YoY, rolling 90‑day revenue).  
  - Deliverables: performance dashboard, variance analysis, and narrative on what is driving growth vs. decline.

- **Marketing Funnel & A/B Testing (`projects/marketing-funnel`)**  
  - Goal: Diagnose drop‑offs in the acquisition funnel and evaluate an experiment to improve conversion.  
  - Stack: SQL for funnel tables, Python for experiment evaluation, and Power BI for experiment reporting.  
  - Deliverables: funnel visualization, test vs. control comparison, and recommendations on whether to ship the variant.

---

## 2. Dashboards

Links and screenshots (or PBIX / Excel files) for my main dashboards live under `dashboards/`.

- **Executive Overview Dashboard** – one‑page view of revenue, customers, churn, and NPS.  
- **Operations & Support Dashboard** – ticket volume, SLAs, backlog, and agent performance.  
- **Marketing Performance Dashboard** – campaign performance, CAC, LTV, and ROI by channel.

Each dashboard folder includes:

- a **README** explaining the intended audience and key questions it answers  
- a **data model sketch** (PDF/PNG or markdown)  
- exported views or screenshots for quick review.

---

## 3. Technical Skills & Tooling

- **SQL**: joins, CTEs, window functions, cohort tables, funnel construction, data quality checks.  
- **Python**: `pandas`, `numpy`, `matplotlib`, `seaborn`, basic `scikit‑learn` (logistic regression, tree‑based models), Jupyter workflows.  
- **Business Intelligence**: Power BI (DAX measures, row‑level filters, star schemas), Excel (pivot tables, Power Query).  
- **Data Practices**: cleaning and reshaping messy data, documenting assumptions, versioning analyses with Git/GitHub.

See the `sql/` and `python/` directories for focused examples and reusable snippets.

---

## 4. How to Explore This Portfolio

1. **Start with the signature projects** in `projects/` to see full, end‑to‑end analyses.  
2. Open the **dashboards** in `dashboards/` (Power BI or Excel) and review the accompanying README files.  
3. Browse **`sql/`** for complex queries (cohorts, funnels, retention, segmentation).  
4. Browse **`python/`** for data cleaning, EDA, and model notebooks/scripts.

---

## 5. Run Sample Data + Python (quick start)

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Generate sample datasets (one time per project):
   - `python projects/customer-churn/generate_sample_data.py`
   - `python projects/sales-performance/generate_sample_data.py`
   - `python projects/marketing-funnel/generate_sample_data.py`
3. Run the analysis scripts:
   - `python python/projects/customer_churn.py`
   - `python python/projects/sales_performance.py`
   - `python python/projects/marketing_funnel_ab_test.py`

---

## 6. About Me

I enjoy working on problems where data can directly improve user experience and business performance. I’m comfortable moving from raw data to a well‑argued recommendation, and I care a lot about making results understandable to non‑technical stakeholders.

If you are interested in working together or have feedback on this portfolio, please feel free to reach out.

