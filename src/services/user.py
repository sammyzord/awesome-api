from .main import AppDBService
from ..schemas import DBServiceError
from ..schemas.user import User
from ..models.user import User as UserModel


class UserDBService(AppDBService):
    def auth_user(self, user_id):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if user is None:
                return None, DBServiceError(status_code=404, message="User not found")

            return User.from_orm(user), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))
