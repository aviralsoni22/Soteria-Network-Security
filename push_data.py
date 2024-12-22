import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set. Please check your .env file.")

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            print("MongoDB connection successful.")
        except Exception as e:
            raise NetworkSecurityException(f"Failed to connect to MongoDB: {e}", sys)

    def csv_to_json_convertor(self, file_path):
        """Convert CSV file to JSON-like format."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File does not exist: {file_path}")

            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        """Insert JSON records into a MongoDB collection."""
        try:
            db = self.mongo_client[database]
            col = db[collection]

            if not records:
                raise ValueError("No records to insert.")

            result = col.insert_many(records)
            print(f"Inserted {len(result.inserted_ids)} records into {database}.{collection}")
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "aviralsoni22"
    COLLECTION = "NetworkData"

    try:
        # Debugging: Check working directory
        print(f"Current Working Directory: {os.getcwd()}")

        # Verify the file exists
        if not os.path.exists(FILE_PATH):
            raise FileNotFoundError(f"File does not exist: {FILE_PATH}")
        else:
            print(f"File found at: {FILE_PATH}")

        network_obj = NetworkDataExtract()

        # Convert CSV to JSON
        records = network_obj.csv_to_json_convertor(FILE_PATH)
        print(f"Preview of Records: {records[:5]}...")  # Display the first 5 records

        # Insert records into MongoDB
        no_of_records = network_obj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
        print(f"Total records inserted: {no_of_records}")
    except NetworkSecurityException as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
