import pandas as pd
from sqlalchemy import create_engine
import os
from ultralytics import YOLO

# --- Define your DB connection ---
# Update these credentials to match your Postgres setup
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'raw'
TABLE_NAME = 'stg_image_detections'  # staging table

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# --- Helper function ---
def extract_message_id(path):
    filename = os.path.basename(path)
    try:
        return int(filename.split("_")[1].split(".")[0])
    except (IndexError, ValueError):
        print(f"Could not extract message_id from: {filename}")
        return None

# --- Run object detection ---
model = YOLO('yolov8n.pt')
image_dir = "../data/raw/telegram_messages/2025-07-14/images"
results_list = []

for root, _, files in os.walk(image_dir):
    for file in files:
        if file.endswith((".jpg", ".png")):
            image_path = os.path.join(root, file)
            message_id = extract_message_id(image_path)
            if message_id is None:
                continue
            try:
                results = model(image_path)
                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls)
                        confidence = float(box.conf)
                        class_name = model.names[cls_id]
                        results_list.append({
                            "image_path": image_path,
                            "message_id": message_id,
                            "object_class": class_name,
                            "confidence_score": confidence
                        })
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

df = pd.DataFrame(results_list)

# --- Save to PostgreSQL ---
df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
print(f"✅ Loaded {len(df)} rows into {TABLE_NAME}")
