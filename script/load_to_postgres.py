import os
import json
import psycopg2
from datetime import datetime

# DB credentials
DB_CONFIG = {
    'dbname': 'raw',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': 5432
}

def load_json_to_postgres(data_dir):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                channel_name = file.replace('.json', '')
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    for msg in messages:
                        try:
                            cur.execute("""
                                INSERT INTO raw.telegram_messages (
                                    id, date, sender_id, channel_name, message, has_media, image_path
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                            """, (
                                msg.get("id"),
                                msg.get("date"),
                                msg.get("sender_id"),
                                channel_name,
                                msg.get("message"),
                                msg.get("has_media", False),
                                msg.get("image_path")
                            ))
                        except Exception as e:
                            print(f"Error inserting message ID {msg.get('id')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded successfully.")

# Call the function with your raw data path
if __name__ == "__main__":
    load_json_to_postgres("data/raw/telegram_messages")
