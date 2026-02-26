import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from server.config import Config
class EmailService:
    def __init__(self, config: Config):
        self.smtp_from_address = config.SMTP_FROM_ADDRESS
        self.smtp_password = config.SMTP_PASSWORD
        self.smtp_host = config.SMTP_HOST
        self.smtp_port = config.SMTP_PORT

    def send_email(self,to: str, subject: str, body: str):
    # 1. Create the email object
        msg = MIMEMultipart()
        msg["From"] = self.smtp_from_address
        msg["To"] = to
        msg["Subject"] = subject

        # 2. Attach the body text
        msg.attach(MIMEText(body, "plain"))

        # 3. Connect to Gmail's SMTP server and send
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()                            # encrypts the connection
            server.login(self.smtp_from_address, self.smtp_password)  # login to gmail
            server.sendmail(self.smtp_from_address, to, msg.as_string())
           

        
