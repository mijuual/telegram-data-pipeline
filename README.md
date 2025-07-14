# 🩺 Ethiopian Medical Telegram Data Scraper

This project is the first step in building a modern ELT (Extract, Load, Transform) data platform for **Kara Solutions**. It focuses on collecting raw data from public Ethiopian medical Telegram channels, laying the foundation for downstream analytics.

---

## Objective

The objective of this project is to extract unstructured medical-related data from public Telegram channels, including:
- Text messages (e.g., promotions, pricing, product availability)
- Media content (e.g., product images such as pills or creams)

This raw data will be used to answer key business questions such as:
- What are the top 10 most frequently mentioned medical products or drugs?
- How do prices or availability vary across different channels?
- Which channels share the most images (visual content)?
- What are the trends in daily and weekly posting activity?

---

##  Methodology

This project implements the **Extract & Load** part of an ELT pipeline. Here's how it works:

1. **Extract**
   - Use the Telegram API to pull messages from selected public channels.
   - Download media (images) for computer vision analysis.
   - Parse and store messages in structured JSON format.

2. **Load**
   - Save raw data to a local Data Lake organized by date and channel.
   - Log scraping activity to track progress and handle rate limits or errors.

3. **Transform & Analyze (next steps)**
   - Load raw data into a PostgreSQL warehouse.
   - Use `dbt` to transform data into a dimensional model (star schema).
   - Run queries to extract business insights.

---

## Tools Used

| Tool         | Purpose                                         |
|--------------|--------------------------------------------------|
| **Python**   | Programming language                             |
| **Telethon** | Telegram scraping via the Telegram API           |
| **dotenv**   | Manage API credentials securely via `.env` file  |
| **JSON**     | Store raw unstructured data                      |
| **Logging**  | Monitor scraping status and errors               |
| **PostgreSQL** _(planned)_ | Data warehouse for structured storage       |
| **dbt** _(planned)_        | SQL-based data transformation and modeling   |

---
##  Requirements

- Python 3.8 or higher
- Telegram API credentials
- Dependencies listed in `requirements.txt`

### Install dependencies

```bash
pip install -r requirements.txt

