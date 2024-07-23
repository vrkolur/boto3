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

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES email message
    msg = {"Body": {"Html": {"Charset": charset, "Data": body_html},
                    "Text": {"Charset": charset, "Data": body_text}},
           "Subject": {"Charset": charset, "Data": "AWS Notification"}}

    to_addresses = ["varunkolur17@gmail.com"]

    from_email = "varun.ravikolur@plansource.com"  

    # Try to send the email
    try:
        #Provide the contents of the Amazon SES message.
        response = ses.send_email(
            Destination={"ToAddresses": to_addresses},
            Message=msg,
            Source=from_email,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        logger.info("Email sent! Message ID: " + response['MessageId'])
        
