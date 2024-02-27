"""
This is the smoke test from API to dynamodb that checks if the API is incrementing the visit count in the dynamodb table.
"""
import boto3
import botocore
import requests

def increments_count_in_db(api_url):
  # hit the API URL to invoke lambda to create/update item in dynamodb
  response = requests.post(api_url, data={})  

  # API response is an integer value
  replied = int(response.text.strip())
  print(replied)
  assert isinstance(replied, int)
  
  # get count from db 
  prev_count = get_db_visit_count()

  # hit the API URL again to check if the count is incremented
  requests.post(api_url, data={})
  next_count = get_db_visit_count()
  print(prev_count, next_count)
  assert next_count == prev_count + 1  

# get the visit count from single source of truth, dynamodb
def get_db_visit_count():
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('MyApplications')
  try:
    response = table.get_item(
      Key={
        'application_id': '1',
      }
    )
  except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Message'])
  else:
    count = int(response['Item']['visit_count'])    
    return count
  


api_url = "https://2tmgp8jcog.execute-api.us-east-1.amazonaws.com/dev"

increments_count_in_db(api_url)

print("Smoke test from API to DynamoDB has passed!")


