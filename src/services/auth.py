import jwt
import secrets
import bcrypt
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError
from .main import AppDBService
from ..schemas.user import AuthUser, UserIn, User
from ..models.user import User as UserModel
from ..dependencies.main import settings


class RegistrationService(AppDBService):

    username_taken = "username taken"

    def register_user(self, user: UserIn):
        try:
            username = user.username
            byte_password = user.password.encode("utf-8")

            password = bcrypt.hashpw(byte_password, bcrypt.gensalt()).decode('utf8')

            new_user = UserModel(username=username, password=password)

            self.db.add(new_user)
            self.db.commit()

            return None

        except IntegrityError:
            return (400, self.username_taken)

        except Exception as err:
            return (500, str(err))

    def username_available(self, username: str):
        try:
            exists = bool(self.db.query(User).filter(User.username == username).first())
            if exists is not None:
                return (400, self.username_taken)

            return None

        except Exception as err:
            return (500, str(err))


class AuthService(AppDBService):

    invalid_credentials = "invalid credentials"

    def login(self, user: AuthUser):
        try:
            username = user.username
            password = user.password.encode("utf-8")

            query = (
                self.db.query(UserModel).filter(UserModel.username == username).first()
            )
            if query is None:
                return None, (400, self.invalid_credentials)

            auth_user = User.from_orm(query)

            match = bcrypt.checkpw(password, auth_user.password.encode("utf-8"))
            if not match:
                return None, (400, self.invalid_credentials)

            refresh_token = secrets.token_hex(20)

            query.refresh_token = refresh_token
            self.db.commit()

            jwt_payload = {
                "id": auth_user.id,
                "username": auth_user.username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
            }

            jwt_token = jwt.encode(
                jwt_payload, settings().secret_key, algorithm="HS256"
            )

            return (jwt_token, refresh_token), None

        except Exception as err:
            return None, (500, str(err))
