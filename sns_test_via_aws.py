import os
import boto3
from botocore.exceptions import ClientError
import logging

# Create a new SES resource
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')

def lambda_handler(event, context):
    # The email body for recipients with non-HTML email clients.
    body_text = "This is a notification from AWS."
                
    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>AWS Notification</h1>
      <p>This is a notification from AWS.</p>
    </body>
    </html>
                """  
              
    charset = "UTF-8"

    msg = {"Body": {"Html": {"Charset": charset, "Data": body_html},
                    "Text": {"Charset": charset, "Data": body_text}},
           "Subject": {"Charset": charset, "Data": "AWS Notification"}}

    to_addresses = ["varun.ravikolur@plansource.com"]

    from_email = "varun.ravikolur@plansource.com"  

    try:
        response = ses.send_email(
            Destination={"ToAddresses": to_addresses},
            Message=msg,
            Source=from_email,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        logger.info("Email sent! Message ID: " + response['MessageId'])
        
