from server.models.chama_member import ChamaMember


class ChamaMemberRepository:
    def __init__(self,db_session):
        self.db_session = db_session
    #Role is no longer a parameter from user 
    def save_chama_member(
        self, user_id, chama_id, role,  invited_by, joined_at=None,
    ):
        # Create chama object
        chama_member = ChamaMember(
            chama_id=chama_id,
            user_id=user_id,
            role=role,
            invited_by=invited_by,
            joined_at=joined_at
        )
        self.db_session.add(chama_member)
        
        return chama_member
