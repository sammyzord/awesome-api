from .main import AppDBService
from ..schemas.user import User
from ..models.user import User as UserModel
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound


class UserDBService(AppDBService):
    def auth_user(self, user_id):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).one()
            return User.from_orm(user)

        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
