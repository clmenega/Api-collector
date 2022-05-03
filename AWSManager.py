from datetime import datetime
import csv
import boto3
import os

_FILE_NAME = ".tmp.csv"

class AWSManager:
    @staticmethod
    def convert_connections_to_csv(users):
        field_name = users[0].keys()
        with open(_FILE_NAME, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_name)
            writer.writeheader()
            writer.writerows(users)

    @staticmethod
    def insert_connection(date: datetime, users: list):
        AWSManager.convert_connections_to_csv(users)
        date_filename = date.strftime("%Y/%m/%d/%H:%M.csv")
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(_FILE_NAME, 'cluster-weather', date_filename)
        os.remove('.tpm.csv')


