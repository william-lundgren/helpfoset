import smtplib
import ssl
import os
import time
from datetime import datetime


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def send_mail(receiver_email, link, sittning):
    # Setup and send mail
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("sender")
    password = os.getenv("password")
    message = f"""\
Subject: Betallänk för {sittning} sittning.

{link}"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("Logging in!", get_time())
        server.login(sender_email, password)

        print("Sending mail", get_time())
        server.sendmail(sender_email, receiver_email, message)


def add(key, dic, count):
    # Add to dictionary depending on if key already exists
    if " " in key:
        key = key.split()[0]
    if key in dic:
        dic[key] += count
    else:
        dic[key] = count


def get_links():
    # TODO implement
    return []


def main():
    # Schedule url for every classroom
    pay_links = get_links()
    sittning = ""

    # Only send mail if there are things scheduled
    for mail in os.getenv("mails").split(","):
        print("Sending email to:", mail)
        send_mail(mail, pay_links.pop(), sittning)


if __name__ == "__main__":
    main()
