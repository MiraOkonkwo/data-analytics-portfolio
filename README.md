# 📊 Data Analytics Portfolio — Miracle Okonkwo

**Live site:** https://miraokonkwo.github.io/data-analytics-portfolio/

## 🚀 About Me

I currently work as a Data and Operations Coordinator, tracking scheduling, workflow, and performance data to support management decisions. That job is what pushed me toward data analytics: the recurring problem was never a lack of data, it was information gaps that hid where a process was actually breaking down. I hold a degree in Computer Science and Statistics, and this portfolio is where I apply that background to real analytical work.

- 📧 joymimi30@gmail.com
- 💻 [github.com/MiraOkonkwo](https://github.com/MiraOkonkwo)
- 🔗 LinkedIn: *add your LinkedIn URL here*

## 💡 What This Portfolio Demonstrates

Each project here starts from a real business question, not a tutorial exercise. I care more about tracing a number back to its cause and stating what it costs the business than about showing off a chart.

## 🧰 Tech Stack

- **Languages:** Python, SQL
- **Libraries:** pandas, matplotlib
- **Databases:** SQLite
- **Tools:** Excel, Google Sheets, Git, GitHub
- **Foundations:** statistics, business reporting, process analysis

## 📂 Featured Projects

### 1️⃣ Fulfillment Risk Analysis
📁 [`01-operations-bottleneck-analysis`](01-operations-bottleneck-analysis/) · 🔗 [Live dashboard](https://miraokonkwo.github.io/data-analytics-portfolio/fulfillment-risk-analysis/)

**Business problem:** A supply chain network was missing delivery promises on more than half its orders, and nobody had traced why.

**Key insights:** I audited 180,519 order line items and found the late-delivery rate was wildly uneven by shipping mode, not by region or department. First Class shipping was late 95.3% of the time, worse than the slow, cheap Standard Class option at 38.1%. The pattern held steady across 37 months and all 23 regions, which pointed to a broken SLA promise rather than a regional or seasonal problem.

**Impact:** $20.1M in sales rides on a late order, and $2.15M was lost on orders that were both late and unprofitable. I laid out four concrete fixes, starting with re-baselining the SLA for the two fastest shipping tiers.

### 2️⃣ SQL Portfolio
📁 [`02-sql-portfolio`](02-sql-portfolio/) · 🔗 [queries.sql](02-sql-portfolio/queries/queries.sql)

**Business problem:** Prove I can pull real answers out of a relational database on demand, the way any data analyst interview will test.

**Key insights:** 18 queries against a 16,282-order database, covering joins, CTEs, and window functions (`RANK`, `NTILE`, `LAG`, running `SUM`/`AVG`). Each one answers something a manager would actually ask: who are the best customers, which employees are under-performing, which customers look like they're about to churn.

**Impact:** Every query runs against real data and returns validated output, in [`results/sample_output.txt`](02-sql-portfolio/results/sample_output.txt), so the numbers in the README aren't made up.

More projects in progress: an automated KPI dashboard and an A/B test or retention analysis.

## ⚠️ Challenges & Tradeoffs

- The raw supply chain dataset was about 92MB with customer PII (names, emails, addresses) mixed in. I dropped every PII column before analysis and kept the raw file out of this repo, documenting where to download it instead.
- Both projects use public or synthetic data, not proprietary company data. I was deliberate about that: it means I could publish the full analysis and code, but it also means the findings are illustrative rather than tied to a real employer's numbers.
- I hit a real Windows/Git environment issue getting this repo pushed (an HTTP/2 network error, then an SSL certificate mismatch between Git's own certificate store and Windows'), and had to force Git to use an older HTTP version and Windows' native certificate handling to get the push through. Small thing, but it's the kind of environment debugging that comes up constantly in real analyst work.

## 📌 Key Takeaways

- I can take a large, messy real-world dataset and trace a business metric back to its actual root cause, not just report it.
- I'm comfortable writing SQL with CTEs and window functions, not just basic `SELECT` statements.
- I think about data privacy and cleaning as a first step, not an afterthought.
- I write up findings the way a manager needs them: a plain-language business problem, the number that matters, and a recommendation.

## 📬 Let's Connect

I'm looking for junior or entry-level data analyst roles, and I'm open to internships with a real path to full-time. If you want to talk about any of this, reach me at joymimi30@gmail.com or open an issue on this repo.
