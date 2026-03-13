import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from server.exceptions import EmailDeliveryError, EmailConfigurationError


class EmailService:

    def __init__(self, smtp_host, smtp_port, smtp_from_address, smtp_password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_from_address = smtp_from_address
        self.smtp_password = smtp_password

    def generate_verification_email(self, user, verify_email_token):
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

        except smtplib.SMTPAuthenticationError as e:
            # Wrong SMTP credentials
            raise EmailConfigurationError(
                "SMTP authentication failed. Check server credentials."
            ) from e

        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            # Can't reach SMTP server
            raise EmailConfigurationError(
                f"Could not connect to SMTP server at {self.smtp_host}:{self.smtp_port}."
            ) from e

        except (
            smtplib.SMTPSenderRefused,
            smtplib.SMTPHeloError,
            smtplib.SMTPNotSupportedError,
        ) as e:
            # Server rejected sender or handshake — configuration issue
            raise EmailConfigurationError(
                "SMTP configuration error. Check your server settings."
            ) from e

        except smtplib.SMTPRecipientsRefused as e:
            # Server refused ALL recipients
            refused = list(e.recipients.keys())

            raise EmailDeliveryError(
                "All recipients were refused by the SMTP server.",
                failed_recipients=refused,
            ) from e

        except smtplib.SMTPException as e:
            # Catch-all for remaining SMTP issues
            raise EmailDeliveryError(
                "Failed to send email.", failed_recipients=[to]
            ) from e

        # sendmail soft-fail:
        # {} -> success
        # {addr: (code, msg)} -> failed recipients
        if failed_recipients:
            raise EmailDeliveryError(
                "Email was only partially delivered — some recipients failed.",
                failed_recipients=list(failed_recipients.keys()),
            )
            

        return {"success": True, "failed_recipients": []}
