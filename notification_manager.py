import os
from twilio.rest import Client
from dotenv import load_dotenv

# load env variable from env file
load_dotenv()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])


    def send_whatsapp(self, user_list, message_body):
        for user in user_list:
            for user_name, user_number in user.items():
                print("Sending wsp message")
                message = self.client.messages.create(
                    from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
                    body=f"{user_name}! {message_body}",
                    to=f"whatsapp:{user_number}",
                )
                print("Sent!", message.sid)

