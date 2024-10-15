# Building a Log Analytics Pipeline for Web Server Logs Using AWS and Apache Spark

## **Project Overview**

**Objective:** Develop an end-to-end ETL pipeline that ingests, processes, analyzes, and visualizes web server access logs to derive insights on website traffic patterns, user behavior, error rates, and performance metrics. The project involves data ingestion, cleaning, transformation, and analysis using AWS services and Apache Spark tools.

**Technologies Used:**

- **AWS Services:** S3
- **Big Data Technologies:** Apache Spark, PySpark
- **Programming Languages:** Python
- **Data Visualization Tools:** Matplotlib, Seaborn

---

## **Project Architecture**

1. **Data Ingestion:**
   - Web server logs are uploaded to an **AWS S3** bucket.

2. **Data Processing:**
   - Use **Apache Spark** to process raw log files from S3.
   - Apply regular expressions to extract useful log fields such as IP address, request status, and timestamps.

3. **Data Transformation:**
   - Perform data cleaning and transformations to prepare for analysis.
   - Store the processed logs in **Parquet** format on S3 for efficient querying.

4. **Data Analysis:**
   - Use **SparkSQL** to query processed log data.
   - Analyze metrics such as the most requested endpoints and user behavior.

5. **Visualization:**
   - Use **Jupyter Notebooks** for visualizing the analysis results with Matplotlib and Seaborn.

---

## **Step-by-Step Implementation Guide**

### **1. Setting Up AWS Resources**

- **Create an S3 Bucket:**
  - Store raw web server logs and output from the analysis.

- **Configure IAM Roles:**
  - Set up roles with permissions for accessing Kinesis, Lambda, EMR, and S3.

### **2. Data Ingestion**

- **Upload Logs to S3:**
  - Use a Python script to handle the uploading of log files to your S3 bucket:

  ```python
  import boto3

  s3_bucket = 'your-bucket'
  s3_raw_path = 'web_server_logs/raw/'

  def upload_logs_to_s3(file_path):
      s3 = boto3.client('s3')
      s3.upload_file(file_path, f'{s3_raw_path}{file_path}')

  upload_logs_to_s3('sample_logs.log')
  ```

### **3. Data Processing with Spark**

- **Initialize Spark Session:**

  ```python
  from pyspark.sql import SparkSession

  spark = SparkSession.builder.appName("WebServerLogAnalysis").getOrCreate()
  ```

- **Read Data from S3:**

  ```python
  logs_df = spark.read.text("s3://your-bucket/web_server_logs/raw/*.log")
  ```

- **Define Regular Expressions and Extract Log Data:**

  ```python
  from pyspark.sql import functions as F

  log_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(.+?)" (\d{3}) (\S+) "(.*?)" "(.*?)"'
  
  parsed_logs_df = logs_df.select(
      F.regexp_extract('value', log_pattern, 1).alias('host'),
      F.regexp_extract('value', log_pattern, 3).alias('user'),
      F.regexp_extract('value', log_pattern, 4).alias('timestamp'),
      F.regexp_extract('value', log_pattern, 6).cast(IntegerType()).alias('status')
  )
  ```

- **Save Processed Data to S3:**

  ```python
  processed_data_path = "s3://your-bucket/web_server_logs/processed/data.parquet"
  parsed_logs_df.write.parquet(processed_data_path, mode='overwrite')
  ```

### **4. Data Analysis with SparkSQL**

- **Load Processed Data:**

  ```python
  data_df = spark.read.parquet(processed_data_path)
  data_df.createOrReplaceTempView("web_logs")
  ```

- **Example Analytics Queries:**

  - Top 10 Most Requested Endpoints:

  ```python
  most_requested = spark.sql("""
      SELECT endpoint, COUNT(*) as request_count
      FROM web_logs
      GROUP BY endpoint
      ORDER BY request_count DESC
      LIMIT 10
  """)
  most_requested.show()

  most_requested.write.csv("s3://your-bucket/web_server_logs/output/most_requested.csv", mode='overwrite')
  ```

### **5. Visualization**

#### **a. Using Jupyter Notebooks**

- **Visualize Results:**

  ```python
  import pandas as pd
  import matplotlib.pyplot as plt
  import seaborn as sns

  most_requested = pd.read_csv('s3://your-bucket/web_server_logs/output/most_requested.csv')

  plt.figure(figsize=(12, 6))
  sns.barplot(data=most_requested, x='request_count', y='endpoint')
  plt.title('Top 10 Most Requested Endpoints')
  plt.xlabel('Request Count')
  plt.ylabel('Endpoint')
  plt.show()
  ```

---

## **Project Documentation**

- **README.md:**
  - **Project Title:** Building a Log Analytics Pipeline for Web Server Logs Using AWS and Apache Spark
  - **Description:** An end-to-end ETL pipeline to analyze web server access logs for insights on website traffic patterns.
  - **Contents:**
    - **Introduction**
    - **Project Architecture**
    - **Technologies Used**
    - **Dataset Information**
    - **Setup Instructions**
      - Prerequisites
      - AWS Configuration
    - **Running the Project**
    - **Data Processing Steps**
    - **Data Analysis and Results**
    - **Visualization**
    - **Conclusion**
  - **License and Contribution Guidelines**

- **Code Organization:**

  ```
  ├── README.md
  ├── data
  │   ├── sample_logs.log
  ├── notebooks
  │   └── visualization.ipynb
  └── scripts
      ├── data_analysis.py
      ├── data_ingestion.py
      └── log_processing.py
  ```

---

## **Best Practices**

- **Use Version Control:**
  - Initialize a Git repository to manage versioning.

- **Error Handling:**
  - Add proper error handling in code and logging where necessary.

- **Security:**
  - Ensure AWS credentials are not hardcoded and use IAM roles instead.

- **Optimization:**
  - Optimize Spark jobs for performance and resource management.

- **Resource Cleanup:**
  - Clean up AWS resources such as S3 buckets and IAM roles that are no longer needed.

---

## **Additional Enhancements**

- **Implement Unit Tests:**
  - Use frameworks like `pytest` for testing data processing functions.

- **Continuous Integration:**
  - Automate testing and code checks using CI tools.

- **Containerization:**
  - Use Docker to containerize data processing scripts.

- **Real-time Data Processing:**
  - Explore integration with AWS Kinesis for real-time log processing.

- **Alerting and Monitoring:**
  - Implement AWS CloudWatch for monitoring and setting up alerts based on specific log metrics.
