from server.models.wallet import ChamaWallet
class ChamaWalletRepository():
    def __init__(self,db_session):
        self.db_session=db_session
    
    def save_chama_wallet(self,chama_id,balance):
        # Create chama wallet object
        chama_wallet = ChamaWallet(
           chama_id=chama_id,
           balance=balance
        )
        self.db_session.add(chama_wallet)
       
        return chama_wallet