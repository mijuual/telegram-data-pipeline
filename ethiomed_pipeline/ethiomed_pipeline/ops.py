# ops.py

from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "../script/scraper.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "../script/load_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], check=True)
    subprocess.run(["dbt", "test"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "../script/load_image_detection.py"], check=True)
