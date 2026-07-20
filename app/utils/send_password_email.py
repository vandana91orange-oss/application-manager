from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_FROM_EMAIL,
    MAIL_PORT=465,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings


def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Password Reset</title>
    </head>
    <body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:40px 0;">
            <tr>
                <td align="center">

                    <table width="600" cellpadding="0" cellspacing="0"
                        style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">

                        <tr>
                            <td style="background:#2563eb;padding:24px;text-align:center;">
                                <h1 style="color:#ffffff;margin:0;font-size:24px;">
                                    Service Manager
                                </h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding:40px;">
                                <h2 style="margin-top:0;color:#333;">
                                    Reset Your Password
                                </h2>

                                <p style="font-size:16px;color:#555;line-height:1.6;">
                                    Hello,
                                </p>

                                <p style="font-size:16px;color:#555;line-height:1.6;">
                                    We received a request to reset your password.
                                    Click the button below to create a new password.
                                </p>

                                <div style="text-align:center;margin:35px 0;">
                                    <a href="{reset_link}"
                                       style="background:#2563eb;
                                              color:#ffffff;
                                              text-decoration:none;
                                              padding:14px 32px;
                                              border-radius:6px;
                                              display:inline-block;
                                              font-size:16px;
                                              font-weight:bold;">
                                        Reset Password
                                    </a>
                                </div>

                                <p style="font-size:15px;color:#555;line-height:1.6;">
                                    This password reset link will expire in
                                    <strong>15 minutes</strong>.
                                </p>

                                <p style="font-size:15px;color:#555;line-height:1.6;">
                                    If you did not request a password reset,
                                    you can safely ignore this email. Your
                                    password will remain unchanged.
                                </p>

                                <hr style="border:none;border-top:1px solid #e5e5e5;margin:30px 0;">

                                <p style="font-size:13px;color:#777;">
                                    If the button doesn't work, copy and paste
                                    the following link into your browser:
                                </p>

                                <p style="word-break:break-all;font-size:13px;color:#2563eb;">
                                    {reset_link}
                                </p>

                            </td>
                        </tr>

                        <tr>
                            <td style="background:#f8f9fa;padding:20px;text-align:center;font-size:12px;color:#777;">
                                © 2026 Service Manager. All rights reserved.
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email
    message["Subject"] = "Reset Your Password"

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)
