from app.celery_app import celery
from app.utils.email import send_email


@celery.task
def send_welcome_email(
    email: str,
    first_name: str,
    temporary_password: str,
):
    body = f"""
        Hi {first_name},

        Welcome to Service Manager!

        Your account has been created successfully, and you can now access the application.

        Login Details
        -------------
        Email: {email}
        Temporary Password: {temporary_password}

        For security reasons, please sign in using the temporary password and change it immediately after your first login.

        If you experience any issues accessing your account, please contact your system administrator.

        We’re excited to have you on board!

        Best regards,
        Service Manager Team
        """

    send_email(
        to_email=email,
        subject="Welcome to Service Manager",
        body=body,
    )
