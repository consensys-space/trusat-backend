from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.text import MIMEText
import base64



def create_message(sender, to, subject, message_text):
    message_text = 'Save this email: TruSat account recovery info for' + to + '\nTo log into TruSat, you\'ll need your password AND this secret code:\n' + message_text + '\nThis email is the only time we can send you this code. Trusat cannot restore your account or reset your password for you. Please save this email forever and make not of the password you used.\nWhy do we do it this way? Read more\nQuestions? Please email: Support@TruSat.org'
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8'))}

def send_message(service, user_id, message):
    message["raw"] = message["raw"].decode('utf-8')
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except Exception as error:
        print('An error occurred: %s' % error)



def send_email(to, message_text):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message_to_send = create_message('kenan.oneal@consensys.net', to, 'TruSat - Save this email: Recovery Info', message_text)

    send_message(service, 'me', message_to_send)
