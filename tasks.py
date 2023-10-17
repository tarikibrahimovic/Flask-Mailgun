import os

import requests
from dotenv import load_dotenv

load_dotenv()
domain = os.getenv("MAILGUN_DOMAIN")


def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Tarik Ibrahimovic <mailgun@{domain}>",
              "to": [to],
              "subject": subject,
              "text": body})
