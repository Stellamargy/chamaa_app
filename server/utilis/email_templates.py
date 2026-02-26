class EmailTemplates:

    @staticmethod
    def email_verification_template(first_name: str, verification_link: str) -> str:
        return f"""
        Hi {first_name},

        Please click the link below to verify your email:

        {verification_link}

        This link will expire in 24 hours.

        If you did not create this account, ignore this email.
        """