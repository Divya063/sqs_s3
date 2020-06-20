import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://us-east-2.queue.amazonaws.com/128895372965/job_post'

response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=1,
    MessageAttributes={
        'Mode': {
            'DataType': 'String',
            'StringValue': 'glassdoor'
        }
    },
    MessageBody=(
        "https://www.indeed.com/viewjob?jk=65a02dd0d86657b5&tk=1eb6s651a1tco000&from=serp&vjs=3"
    )
)

print(response['MessageId'])