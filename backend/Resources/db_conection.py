from twisted.enterprise import adbapi
import os

dbpool = adbapi.ConnectionPool(
    "psycopg2",
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "db"),
    port=int(os.getenv("POSTGRES_PORT", 5432))
)