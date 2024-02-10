from pyspark.sql import SparkSession 
from pyspark.sql.functions import from_json , current_timestamp
from pyspark.sql.types import StructType, StructField, StringType , TimestampType 
from dotenv import load_dotenv
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 pyspark-shell'

load_dotenv() 

server = os.getenv('KAF_SERVER')
topic = os.getenv('TOPIC_NAME')
my_path = os.getenv('PROJECT_PATH')
 
spark = (SparkSession
         .builder
         .appName('tableOfProcesses')
         .getOrCreate()
        ) 

spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
spark.conf.set("spark.sql.repl.eagerEval.truncate", 0)


schema = StructType([StructField('cpu_percent' , StringType()) ,
                     StructField('username' , StringType()) ,
                     StructField('name' , StringType()) , 
                     StructField('pid' , StringType()) , 
                ])

spark.sparkContext.setLogLevel('ERROR')

process_df = (spark
              .readStream
              .format('kafka')
              .option('kafka.bootstrap.servers' , server)
              .option('subscribe' , topic)
              .option('startingOffsets' , 'earliest')
              .load()
              .selectExpr('CAST(value AS STRING) as message')
            )

parsed_stream_df = process_df.select(from_json("message",schema).alias("parsed_data"))

result_df = parsed_stream_df.select("parsed_data.*").withColumn('timestamp' , current_timestamp())

result_df = (result_df
             .selectExpr('username' , 'name' ,'timestamp' , 'pid' , 'CAST(cpu_percent as REAL) as CPU')
             .filter("username = 'amir' AND name != 'java' ")
             )

data = ( result_df
        .writeStream
        .format('console')
        .outputMode('update')
        .option("truncate", False)
        .start()
    )

data.awaitTermination()
