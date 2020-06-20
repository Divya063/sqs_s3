import boto3

# Create SQS client
sqs = boto3.client('sqs')

# Create a SQS queue
response = sqs.create_queue(
    QueueName='job_post',
    Attributes={
        'ReceiveMessageWaitTimeSeconds': '1'
    }
)

print(response['QueueUrl'])