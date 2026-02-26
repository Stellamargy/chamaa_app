from server.services.email_service import EmailService
from server.services.jwt_service import JwtService
from server.config import Config
from server.services.email_verification import EmailVerification
# Create instances (reuse the object instead creating one everytime you want to use the object)
jwt_service=JwtService(Config)   # load configurations
email_service=EmailService(Config) # load configurations
email_verification=EmailVerification(jwt_service,email_service)

