from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from server.exceptions.database import DatabaseError
from server.exceptions.auth import AuthenticationError
from server.exceptions.base import AppError
from server.models.chama_member import MemberRole
from datetime import datetime



class ChamaService:
    def __init__(
        self,
        db_session,
        chama_repository,
        chama_member_repository,
        chama_wallet_repository,
        user_repository
    ):
        self.db_session = db_session
        self.chama_repository = chama_repository
        self.chama_member_repository = chama_member_repository
        self.chama_wallet_repository = chama_wallet_repository
        self.user_repository=user_repository

    def create_chama(self, chama_input, current_user_id):
        from server.schema.chama_schema import CreateChamaSchema
        #1.Validate chama input
        #create chamaschema instance
        schema = CreateChamaSchema()
        #validate chama data 
        valid_data = schema.load(chama_input)
        #Check if the user is valid (jwt can be stale)
        existing_user=self.user_repository.get_user_by_id(user_id=current_user_id)
        if not existing_user:
                raise AuthenticationError("Unable to authenticate user.")

        try:
        # 1. Create chama
            chama = self.chama_repository.save_chama(valid_data, current_user_id)

            # 2. Add creator as ACTIVE member immediately
            self.chama_member_repository.save_chama_member(
                chama_id=chama.id,
                user_id=current_user_id,
                #I will pass the chama administrator (like a chama super admin )
                role=MemberRole.CHAMA_ADMIN,
                invited_by=None,
                joined_at=datetime.utcnow(),  # creator is instantly active
            )

            # 3. Create wallet
            self.chama_wallet_repository.save_chama_wallet(
                chama_id=chama.id,
                balance=Decimal("0.00"),
            )

            #Commit all once
            self.db_session.commit()

            return chama

        except SQLAlchemyError as e:
            # rollback 
            self.db_session.rollback()
            raise DatabaseError("Chama creation failed. Please try again.") from e
            #Do I really need to handle this / have this default-I am not expecting something out of the ordinary
        except Exception as e:
            raise AppError("something went wrong durin chama creation,try again later") from e




#Messae shd be clear ,actionable ,non-technical and consistent ----- tips for writing good exceptions message