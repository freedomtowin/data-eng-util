import boto3
from io import StringIO
import os, datetime
from io import StringIO
import json



class KinesisDataClient():

    def __init__(self,service,region):

        # function to create a client with aws for a specific service and region
        self.kinesis = boto3.client(service, region_name=region)


    def send_kinesis(self, kinesis_stream_name, kinesis_shard_count, data):

        kinesisRecords = [] # empty list to store data

        (rows, columns) = data.shape # get rows and columns off provided data

        rowCount = 0 # as we start with the first

        # loop over each of the data rows received 
        for _, row in data.iterrows(): 

            tmp = row.to_dict()
        
            response = self.kinesis.put_record(
                    Data = json.dumps(tmp), # data byte-encoded
                    PartitionKey = 'source', # some key used to tell Kinesis which shard to use
                    StreamName = kinesis_stream_name
                )
            
            # regardless, make sure to incrememnt the counter for rows.
            rowCount = rowCount + 1
            

        # log out how many records were pushed
        print('Total Records sent to Kinesis: {0}'.format(rowCount))



class Utils:

    def save_results(self, df, params, city, search_type):
        """ save parsed search results """
        fname = params['auto_make_model'] if 'auto_make_model' in params else 'generic'
        city = city.replace(' ', '')
        ts = datetime.datetime.now().isoformat()
        if os.environ['ENV'] == 'local':
            dirname = os.getcwd()
            df.to_csv(f'{dirname}/db/results/{search_type}_{fname}_{city}_{ts}_results.csv')
        else:
            self.send_to_s3(df, fname, city, search_type, ts)

    def send_to_s3(self, df, fname, city, search_type, ts):
        # get variable names
        s3_bucket = os.environ['S3_BUCKET']
        # get env variables if dev environment (local)
        if os.environ['ENV'] == 'dev':
            s3_secret = os.environ['S3_SECRET']
            s3_key = os.environ['S3_KEY']
            s3_resource = boto3.resource('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret)
            s3_client = boto3.client('s3', aws_access_key_id=s3_key, aws_secret_access_key=s3_secret)
        else:
            s3_resource = boto3.resource('s3')
            s3_client = boto3.client('s3')
        
        # create csv buffer to send to S3
        csv_buffer = StringIO()
        filename = f'{search_type}_{fname}_{city}_{ts}_results.csv'
        df.to_csv(csv_buffer)

        # send to S3
        print('sending to s3...')
        prefix = f'{search_type}/'
        self.folder_exists(s3_client, s3_bucket, prefix)
        s3_resource.Object(s3_bucket, f'{prefix}{filename}').put(Body=csv_buffer.getvalue())

    def folder_exists(self, client, bucket, folder):
        res = client.list_objects_v2(Bucket=bucket, Prefix=folder)
        if res['KeyCount'] > 0:
            return True
        else:
            client.put_object(Bucket=bucket, Body='', Key=folder)