import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from server.exceptions.email import EmailDeliveryError


class EmailService:
    # pass verification link as an attribute(future code refactoring)
    def __init__(self, smtp_host, smtp_port, smtp_from_address, smtp_password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_from_address = smtp_from_address
        self.smtp_password = smtp_password

    #Creates email verification email 
    def generate_verification_email(self, user, verify_email_token):
        #make this url dynamic -do not hard code it (future me note)
        verification_link = (
            f"http://127.0.0.1:5000/auth/verify_email?token={verify_email_token}"
        )

        html_body = render_template(
            "email/verify_email.html",
            first_name=user.first_name,
            verification_link=verification_link,
        )

        return html_body

    def send_email(self, to: str, subject: str, html_body: str):

        msg = MIMEMultipart()
        msg["From"] = self.smtp_from_address
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_from_address, self.smtp_password)
                failed_recipients = server.sendmail(
                    self.smtp_from_address, to, msg.as_string()
                )


        except smtplib.SMTPException as e:

            raise EmailDeliveryError(
                "We couldn’t send the email. Please try again later."
            ) from e

        # sendmail soft-fail:
        # {} -> success
        # {addr: (code, msg)} -> failed recipients
        if failed_recipients:
            raise EmailDeliveryError(
                "We couldn’t send the email. Please try again later."
            )
            

        return {"success": True}
