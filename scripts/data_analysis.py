from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

# Load Processed Data
logs_df = spark.read.parquet("s3://your-bucket/logs/processed/")

# Register DataFrame as Temporary View
logs_df.createOrReplaceTempView("logs")

# Example Queries
# Top 10 Requested Endpoints
response = spark.sql("""
SELECT endpoint, COUNT(*) as request_count
FROM logs
GROUP BY endpoint
ORDER BY request_count DESC
LIMIT 10
""")
response.show()

# Save Query Results
response.write.csv("s3://your-bucket/logs/output/top_endpoints.csv", mode='overwrite')
