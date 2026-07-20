import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings


def send_email(to_email: str, subject: str, body: str):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
    ) as smtp:
        smtp.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
        )

        smtp.send_message(message)

# def send_email(
#     to_email: str,
#     subject: str,
#     body: str,
# ):
#     message = MIMEMultipart()

#     message["From"] = settings.SMTP_FROM_EMAIL
#     message["To"] = to_email
#     message["Subject"] = subject

#     message.attach(MIMEText(body, "plain"))

#     with smtplib.SMTP(
#         settings.SMTP_HOST,
#         settings.SMTP_PORT,
#     ) as smtp:

#         smtp.starttls()

#         smtp.login(
#             settings.SMTP_USERNAME,
#             settings.SMTP_PASSWORD,
#         )

#         smtp.send_message(message)
