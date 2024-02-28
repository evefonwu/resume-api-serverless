# Lamda function to update visit count in DynamoDB

import boto3 
import botocore

client = boto3.client('dynamodb')

DYNAMODB_TABLE_NAME = "MyApplications" 
CORS_ALLOWED_ORIGIN = "https://resume.evefonwu.com" # "*"

def lambda_handler(event,context): 
    updatedCount = 0
    
    try:
        ddbResponse = client.put_item(
            TableName=DYNAMODB_TABLE_NAME,
            Item={
              "application_id": {
                'S': "1"
              },
              "visit_count": {
                'N': "1"
              }
            },
            ConditionExpression="attribute_not_exists(application_id)"
        )        
        updatedCount = 1
        
    except botocore.exceptions.ClientError as e:   

        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"The table '{DYNAMODB_TABLE_NAME}' does not exist.")  
            return 
           
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':            
            ddbResponse = client.update_item(        
                TableName=DYNAMODB_TABLE_NAME,
                Key={'application_id': {'S': '1'}},
                UpdateExpression="SET visit_count = visit_count + :step",
                ExpressionAttributeValues={
                    ":step": {"N":"1"}
                },
                ReturnValues='UPDATED_NEW'
            )                
            updatedCount = ddbResponse['Attributes']['visit_count']['N']
    
    #print("Visit #:" + str(updatedCount))
    
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': CORS_ALLOWED_ORIGIN, 
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': updatedCount
    }

    #print(response)
    return response

# in dev:
# lambda_handler({}, {})