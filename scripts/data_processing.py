import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col

# Initialize Spark Session
spark = SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

# Read Raw Data from S3
logs_df = spark.read.text("s3://your-bucket/logs/raw/*")

# Define Regular Expression Pattern
log_pattern = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d{3}) (?P<size>\S+)')

# Parse Log Entries

def parse_log_line(log_line):
    match = log_pattern.match(log_line)
    return match.groupdict() if match else None

logs_parsed = logs_df.rdd.map(lambda row: parse_log_line(row.value)).filter(lambda x: x is not None)

# Convert to DataFrame and Transform
logs_df = logs_parsed.toDF()\nlogs_df = logs_df.withColumn('method', split(col('request'), ' ').getItem(0)) \
               .withColumn('endpoint', split(col('request'), ' ').getItem(1)) \
               .withColumn('protocol', split(col('request'), ' ').getItem(2))

# Write Processed Data to S3 in Parquet Format
logs_df.write.parquet("s3://your-bucket/logs/processed/", mode='overwrite')
