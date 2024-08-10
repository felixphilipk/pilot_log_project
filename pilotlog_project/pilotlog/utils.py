import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Need to update in env file
os.environ['PYSPARK_PYTHON'] = os.getenv('PYSPARK_PYTHON')
os.environ['PYSPARK_DRIVER_PYTHON'] = os.getenv('PYSPARK_DRIVER_PYTHON')

def transform_data(file_path):
    """
    Transforms the JSON data using Spark, inferring the schema automatically.
    """
    # Start Spark session
    spark = SparkSession.builder.appName('PilotLogImport').getOrCreate()

    # Read JSON data and infer schema
    df = spark.read.option("multiLine", True).json(file_path)

    # Print inferred schema for debugging
    df.printSchema()

    # Flatten the 'meta' struct into individual columns
    if 'meta' in df.columns:
        for field in df.select("meta.*").columns:
            df = df.withColumn(field, col(f"meta.{field}"))
        df = df.drop("meta")

    # Handle any other required transformations
    if '_modified' in df.columns:
        df = df.withColumnRenamed('_modified', 'modified')
    
    if 'Record_Modified' in df.columns:
        df = df.withColumn('record_modified', from_unixtime(col('Record_Modified')))

    # Convert DataFrame rows to JSON-like dictionaries
    transformed_data = [row.asDict() for row in df.collect()]

    logger.debug("Transformed Data:")
    for item in transformed_data:
        logger.debug(item)

    return transformed_data
