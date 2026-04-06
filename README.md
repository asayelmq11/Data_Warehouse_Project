# 🎵 Sparkify Data Warehouse Project

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-Redshift-orange?logo=amazon-aws)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Project Overview
This project builds a **data warehouse** for **Sparkify**, a music streaming startup.  
The goal is to analyze **user activity and songplays** using a **star schema** in **Amazon Redshift**, enabling fast and efficient analytics.

The ETL pipeline:
1. Extracts data from **S3** (song & log JSON data).  
2. Loads data into **staging tables** in Redshift.  
3. Transforms and inserts data into **fact and dimension tables**.

---

## 📦 Data Sources
- **Song data:** `s3://udacity-dend/song_data`  
- **Log data:** `s3://udacity-dend/log_data`  
- **Log JSONPath:** `s3://udacity-dend/log_json_path.json`

---

## 🗂 Data Warehouse Schema

### Fact Table
- **`songplays`**: Records of each song play, references to users, songs, and artists.

### Dimension Tables
- **`users`**: User info (id, name, gender, subscription level)  
- **`songs`**: Song info (id, title, artist_id, year, duration)  
- **`artists`**: Artist info (id, name, location, latitude, longitude)  
- **`time`**: Timestamp breakdown (hour, day, week, month, year, weekday)

> Star schema ensures **efficient queries** and supports analytics like **popular songs, user engagement, and artist popularity**.

---

## 📂 Project Files
| File | Description |
|------|-------------|
| `create_redshift_cluster.py` | (Optional) Automates Redshift cluster creation |
| `dwh.cfg` | AWS, Redshift, S3, and IAM role configuration |
| `sql_queries.py` | SQL queries for creating, dropping, and inserting tables |
| `create_tables.py` | Drops and creates staging & star schema tables |
| `etl.py` | ETL pipeline: loads data from S3 → Redshift → star schema |
| `README.md` | Project documentation (this file) |

---

## ⚡ How to Run

```bash
# 1️⃣ Install dependencies
pip install boto3 psycopg2-binary configparser

# 2️⃣ Configure AWS credentials in dwh.cfg

# 3️⃣ (Optional) Create Redshift cluster
python create_redshift_cluster.py

# 4️⃣ Create tables
python create_tables.py

# 5️⃣ Run ETL pipeline
python etl.py

# 6️⃣ Verify data in Redshift
SELECT COUNT(*) FROM songplays;
SELECT * FROM users LIMIT 10;
SELECT * FROM songs LIMIT 10;
```
---

## ✨ Features
1. Automated ETL from S3 → Redshift
2. Star schema optimized for analytics
3. Staging tables for data validation
4. Duplicate handling to maintain integrity
5. Uses AWS services: Redshift, S3, IAM

