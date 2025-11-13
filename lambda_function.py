import os
import json
from email_sender import EmailSender

def lambda_handler(event, context):
    print("Starting email sending process")

    # get env variables
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    recipients_string = os.environ.get('RECIPIENTS')

    recipients = [email.strip() for email in recipients_string.split(',') if email.strip()]

    cc_string = os.environ.get('CC_LIST')

    cc = [email.strip() for email in cc_string.split(',') if email.strip()] if cc_string else []

    subject_line = os.environ.get('SUBJECT_LINE')
    body_msg = os.environ.get('BODY_MSG')

    if not all([gmail_user, gmail_password, recipients, cc, subject_line, body_msg]):
        return {
                'statusCode': 500,
                'body': json.dumps("Missing environment variables")
                }

    try:
        # initialize email sender
        sender = EmailSender(gmail_user, gmail_password, recipients, cc)

        # send email
        deferred = sender.send_email(subject_line, body_msg)

        # chain callbacks
        sender.chain_callbacks(
                deferred,
                sender.send_confirmation,
                sender.confirmation_success,
                sender.failure
                )
        
        return {
                'statusCode': 200,
                'body': json.dumps('Email process completed')
                }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
                'statusCode': 500,
                'body': json.dumps(f'Error: {str(e)}')
                }


