from server.models.chama import Chama ,ChamaStatus
class ChamaRepository():
    def __init__(self,db_session):
        self.db_session=db_session
    
    def save_chama(self,chama_data,current_user_id):
        # Create chama object
        chama = Chama(
            name=chama_data["name"],
            description=chama_data["description"],
            created_by=current_user_id,
            status=ChamaStatus.ACTIVE
        )
        self.db_session.add(chama)
        #Flush to get chama id
        self.db_session.flush()
        return chama