# from server.models import db 
# from server import create_app
# app=create_app()
# with app.app_context():
#     # db.drop_all()
#     db.create_all()
    
#     print("successful")

def log (func):
    def wrapper (name):
        print("Function started")
        func(name)
        print("Function ended")
    return wrapper

@log
def say_hi(name):
    print(f"Hi {name}")

say_hi("Stella")
