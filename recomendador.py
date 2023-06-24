from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import col
# Create a Spark session
spark = SparkSession.builder.appName("CSV Reader").getOrCreate()
data_path = "/home/user/movies_metadata.csv"

csv_options = {
    "header": "true",
    "encoding": "utf-8",
    "sep": ","
}

df = spark.read.format("csv").options(**csv_options).load(data_path)
df.head()
# Convert rating column to float
df = df.withColumn("vote_average", df["vote_average"].cast("float"))

# Filter out any invalid or missing values
df = df.filter(df["original_title"].isNotNull() & df["vote_average"].isNotNull() & df["genres"].isNotNull() & df["production_companies"].isNotNull())

train_data, test_data = df.randomSplit([0.8, 0.2], seed=42)

# Create StringIndexers for the user and song columns
original_title_indexer = StringIndexer(inputCol="original_title", outputCol="original_titleIndex")
vote_average_indexer = StringIndexer(inputCol="vote_average", outputCol="vote_averageIndex")
genres_indexer = StringIndexer(inputCol="genres", outputCol="genresIndex")
production_companies_indexer = StringIndexer(inputCol="production_companies", outputCol="production_companiesIndex")

# Fit StringIndexers and transform the data
indexed_data = original_title_indexer.fit(train_data).transform(train_data)
indexed_data = vote_average_indexer.fit(indexed_data).transform(indexed_data)
indexed_data = genres_indexer.fit(indexed_data).transform(indexed_data)
indexed_data = production_companies_indexer.fit(indexed_data).transform(indexed_data)

# Create an ALS recommender model
als = ALS(userCol="original_titleIndex", itemCol="genresIndex", ratingCol="vote_averageIndex", nonnegative=True)

# Fit the model to the training data
model = als.fit(indexed_data)

original_title_indexer = StringIndexer(inputCol="original_title", outputCol="original_titleIndex")
vote_average_indexer = StringIndexer(inputCol="vote_average", outputCol="vote_averageIndex")
genres_indexer = StringIndexer(inputCol="genres", outputCol="genresIndex")
production_companies_indexer = StringIndexer(inputCol="production_companies", outputCol="production_companiesIndex")

# Fit StringIndexers and transform the data
indexed_test_data = original_title_indexer.fit(test_data).transform(test_data)
indexed_test_data = vote_average_indexer.fit(indexed_test_data).transform(indexed_test_data)
indexed_test_data = genres_indexer.fit(indexed_test_data).transform(indexed_test_data)
indexed_test_data = production_companies_indexer.fit(indexed_test_data).transform(indexed_test_data)

recommendations = model.recommendForUserSubset(indexed_test_data, 5)

recommendations.show(truncate=False)


-------
id_to_retrieve = 10194

filtered_data = indexed_data.filter(col("original_titleIndex") == id_to_retrieve)

genresIndex = filtered_data.select("original_title").collect()[0][0]

print(genresIndex)

df_original = spark.read.format("csv").options(**csv_options).load(data_path)

title = (df_original.filter(col("original_title") == genresIndex)).select("original_language").collect()[0][0]
print(title)

df_original1 = spark.read.format("csv").options(**csv_options).load(data_path)

title1 = (df_original1.filter(col("original_title") == genresIndex)).select("genres").collect()[0][0]
print(title1)
