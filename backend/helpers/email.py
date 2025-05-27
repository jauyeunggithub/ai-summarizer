import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_plain_text_email(to_email, subject, message_text):
    try:
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        from_email = os.getenv("FROM_EMAIL", "no-reply@summarizerai.online")
        if not sendgrid_api_key:
            raise Exception("SENDGRID_API_KEY not set in environment")

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=message_text
        )

        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

        print(f"Email sent to {to_email}, status: {response.status_code}")
        return response.status_code == 202

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
