from server.utilis.email_templates import EmailTemplates
class EmailVerification:
    BASE_URL='http://127.0.0.1:5000'
    def __init__(self,jwt_service,email_service):
        self.jwt_service=jwt_service
        self.email_service=email_service

    def send_email_verification_link(self,user):
        email_verification_payload={
            "token_type":"EMAIL_VERIFICATION",
            "user_id":user.id,
           

        }
        token=self.jwt_service.generate_token(email_verification_payload,144)
        verification_link = f"{EmailVerification.BASE_URL}/verify_email?token={token}"
        body = EmailTemplates.email_verification_template(
            first_name=user.first_name,
            verification_link=verification_link
        )
        self.email_service.send_email(
            to=user.email_address,
            subject="Verify your email address",
            body=body
        )
        print("Successful!!!!")
    #Generate token ---- I will need payload and expires in 
    #Since I am going to call this fn in onboard user I can access the user object 


    #Construct verification email ---Use chatgpt 
    #Connect and break down functions .

# #try it 
# from server.services.email_service import EmailService
# from server.services.jwt_service import JwtService
# from server.models.user import User
# from server.config import Config 
# email_service=EmailService(Config)
# jwt_service=JwtService(Config)
# email_verification =EmailVerification(jwt_service,email_service)
# email_verification.send_email_verification_link({
#     "id":1,
#     "is_verified":True,
#     "email":"stellahmargy0211@gmail.com",
#     "first_name":"Oly"
# })
