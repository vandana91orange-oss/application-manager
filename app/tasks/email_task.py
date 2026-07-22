import smtplib
import ssl
from email.message import EmailMessage

from app.config import settings

from app.celery_app import celery


@celery.task
def send_welcome_email(
    to_email: str,
    subject: str,
    first_name: str,
    temporary_password: str,
):
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to Service Manager</title>
    </head>

    <body style="
        margin:0;
        padding:0;
        background-color:#f4f6f9;
        font-family:Arial, Helvetica, sans-serif;
    ">

        <table
            width="100%"
            cellpadding="0"
            cellspacing="0"
            style="background:#f4f6f9;padding:40px 15px;"
        >
            <tr>
                <td align="center">

                    <table
                        width="600"
                        cellpadding="0"
                        cellspacing="0"
                        style="
                            width:100%;
                            max-width:600px;
                            background:#ffffff;
                            border-radius:10px;
                            overflow:hidden;
                            box-shadow:0 2px 8px rgba(0,0,0,0.08);
                        "
                    >
                        <tr>
                            <td
                                align="center"
                                style="
                                    background:#F97316;
                                    color:#ffffff;
                                    padding:30px;
                                "
                            >
                                <h1 style="margin:0;font-size:28px;">
                                    Welcome to Service Manager
                                </h1>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding:35px;color:#333333;">

                                <p style="font-size:16px;margin-top:0;">
                                    Hi <strong>{first_name}</strong>,
                                </p>

                                <p style="font-size:15px;line-height:1.7;">
                                    Your account has been created successfully.
                                    You can now access
                                    <strong>Service Manager</strong>.
                                </p>

                                <table
                                    width="100%"
                                    cellpadding="10"
                                    cellspacing="0"
                                    style="
                                        margin:30px 0;
                                        border:1px solid #dddddd;
                                        border-collapse:collapse;
                                    "
                                >
                                    <tr style="background:#FFF7ED;">
                                        <th
                                            colspan="2"
                                            style="
                                                text-align:left;
                                                font-size:16px;
                                                padding:12px;
                                            "
                                        >
                                            Login Details
                                        </th>
                                    </tr>

                                    <tr>
                                        <td
                                            width="35%"
                                            style="border-top:1px solid #dddddd;"
                                        >
                                            <strong>Email</strong>
                                        </td>

                                        <td style="border-top:1px solid #dddddd;">
                                            {to_email}
                                        </td>
                                    </tr>

                                    <tr>
                                        <td style="border-top:1px solid #dddddd;">
                                            <strong>Temporary Password</strong>
                                        </td>

                                        <td style="border-top:1px solid #dddddd;">
                                            <strong>{temporary_password}</strong>
                                        </td>
                                    </tr>
                                </table>

                                <div style="
                                    background:#FFF8E5;
                                    border-left:5px solid #F97316;
                                    padding:15px;
                                    margin:25px 0;
                                ">
                                    <strong>Security Reminder</strong>

                                    <p style="margin:8px 0 0;line-height:1.6;">
                                        Please sign in using your temporary
                                        password and change it immediately
                                        after your first login.
                                    </p>
                                </div>

                                <div style="text-align:center;margin:35px 0;">
                                    <a
                                        href="{settings.FRONTEND_URL}/login"
                                        style="
                                            background:#F97316;
                                            color:#ffffff;
                                            text-decoration:none;
                                            padding:14px 28px;
                                            border-radius:6px;
                                            display:inline-block;
                                            font-size:15px;
                                            font-weight:bold;
                                        "
                                    >
                                        Login to Service Manager
                                    </a>
                                </div>

                                <p style="font-size:15px;line-height:1.7;">
                                    If you experience any issues accessing your
                                    account, please contact your system
                                    administrator.
                                </p>

                                <p style="margin-top:30px;">
                                    Best regards,<br>
                                    <strong>Service Manager Team</strong>
                                </p>

                            </td>
                        </tr>

                        <tr>
                            <td
                                align="center"
                                style="
                                    background:#f8fafc;
                                    padding:20px;
                                    font-size:12px;
                                    color:#777777;
                                "
                            >
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

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email

    message.set_content(
        f"""
Hi {first_name},

Welcome to Service Manager.

Email: {to_email}
Temporary Password: {temporary_password}

Please change your password immediately after your first login.

Best regards,
Service Manager Team
"""
    )

    message.add_alternative(
        html_body,
        subtype="html",
    )

    smtp_host = settings.SMTP_HOST
    smtp_port = int(settings.SMTP_PORT)
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD

    ssl_context = ssl.create_default_context()

    try:
        if smtp_port == 465:
            # SSL connection starts immediately.
            with smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                context=ssl_context,
                timeout=30,
            ) as smtp:
                smtp.login(
                    smtp_username,
                    smtp_password,
                )
                smtp.send_message(message)

        elif smtp_port == 587:
            # Plain connection upgraded to TLS.
            with smtplib.SMTP(
                smtp_host,
                smtp_port,
                timeout=30,
            ) as smtp:
                smtp.ehlo()
                smtp.starttls(context=ssl_context)
                smtp.ehlo()

                smtp.login(
                    smtp_username,
                    smtp_password,
                )

                smtp.send_message(message)

        else:
            raise ValueError(
                "Unsupported SMTP port. Use port 587 with STARTTLS "
                "or port 465 with SSL."
            )

    except smtplib.SMTPAuthenticationError as exc:
        raise RuntimeError(
            "SMTP authentication failed. Check the SMTP username, "
            "password or application password."
        ) from exc

    except smtplib.SMTPServerDisconnected as exc:
        raise RuntimeError(
            f"SMTP server unexpectedly closed the connection. "
            f"Check SMTP_HOST={smtp_host}, SMTP_PORT={smtp_port}, "
            "and ensure the encryption method matches the port."
        ) from exc

    except (smtplib.SMTPException, OSError) as exc:
        raise RuntimeError(
            f"Unable to send email through {smtp_host}:{smtp_port}: {exc}"
        ) from exc