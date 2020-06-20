import boto3
from scrape import Scraper

# Create SQS client

sqs = boto3.client('sqs')


queue_url = 'https://us-east-2.queue.amazonaws.com/128895372965/job_post'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=2
)
print(response)
message = response['Messages'][0]
url = response['Messages'][0]['Body']
mode = response['Messages'][0]['MessageAttributes']['Mode']['StringValue']
print(mode, url)
receipt_handle = message['ReceiptHandle']
sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message)
scrape = Scraper(url)
print(scrape)



