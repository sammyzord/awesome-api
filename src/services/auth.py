import jwt
import secrets
import bcrypt
from mnemonic import Mnemonic
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError
from .main import AppDBService
from ..schemas import DBServiceError
from ..schemas.user import User
from ..schemas.auth import RegisterRequest, AuthRequest, RecoveryRequest
from ..models.user import User as UserModel
from ..dependencies.main import settings


class RegistrationService(AppDBService):

    username_taken = "username taken"
    mnemo = Mnemonic("english")

    def register_user(self, request: RegisterRequest):
        try:
            username = request.username
            byte_password = request.password.encode("utf-8")

            password = bcrypt.hashpw(byte_password, bcrypt.gensalt()).decode("utf-8")

            new_user = UserModel(username=username, password=password)

            self.db.add(new_user)
            self.db.commit()

            return None

        except IntegrityError:
            return DBServiceError(status_code=400, message=self.username_taken)
        except Exception as err:
            return DBServiceError(status_code=500, message=str(err))

    def username_available(self, username: str):
        try:
            exists = bool(self.db.query(User).filter(User.username == username).first())
            if exists is not None:
                return DBServiceError(status_code=400, message=self.username_taken)

            return None

        except Exception as err:
            return DBServiceError(status_code=500, message=str(err))

    def generate_recovery_key(self, user_id: int):
        try:
            query = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if query is None:
                return None, DBServiceError(status_code=404, message="User not found")

            word_list = self.mnemo.generate(strength=256)
            byte_word_list = word_list.encode("utf-8")

            recovery_key = bcrypt.hashpw(byte_word_list, bcrypt.gensalt()).decode(
                "utf8"
            )

            query.recovery_key = recovery_key
            self.db.commit()
            return word_list, None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def activate_user(self, word_list: str, user_id: int):
        try:
            query = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if query is None:
                return None, DBServiceError(status_code=404, message="User not found")

            byte_word_list = word_list.encode("utf-8")

            match = bcrypt.checkpw(byte_word_list, query.recovery_key.encode("utf-8"))
            if not match:
                return None, DBServiceError(
                    status_code=400, message="invalid recovery phrase"
                )

            query.active = True
            self.db.commit()
            return True, None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def reset_password(self, request: RecoveryRequest):
        try:
            username = request.username

            query = (
                self.db.query(UserModel).filter(UserModel.username == username).first()
            )
            if query is None:
                return None, DBServiceError(
                    status_code=400, message="invalid recovery credentials"
                )

            word_list = request.recovery_key
            byte_word_list = word_list.encode("utf-8")

            match = bcrypt.checkpw(byte_word_list, query.recovery_key.encode("utf-8"))
            if not match:
                return None, DBServiceError(
                    status_code=400, message="invalid recovery credentials"
                )

            byte_password = request.password.encode("utf-8")

            password = bcrypt.hashpw(byte_password, bcrypt.gensalt()).decode("utf-8")

            query.password = password
            self.db.commit()
            return True, None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))


class AuthService(AppDBService):

    invalid_credentials = "invalid credentials"

    def login(self, auth_request: AuthRequest):
        try:
            username = auth_request.username
            password = auth_request.password.encode("utf-8")

            query = (
                self.db.query(UserModel).filter(UserModel.username == username).first()
            )
            if query is None:
                return None, DBServiceError(
                    status_code=400, message=self.invalid_credentials
                )

            match = bcrypt.checkpw(password, query.password.encode("utf-8"))
            if not match:
                return None, DBServiceError(
                    status_code=400, message=self.invalid_credentials
                )

            refresh_token = secrets.token_hex(20)
            byte_refresh_token = refresh_token.encode("utf-8")

            encrypted_token = bcrypt.hashpw(
                byte_refresh_token, bcrypt.gensalt()
            ).decode("utf8")

            query.refresh_token = encrypted_token
            self.db.commit()

            auth_user = User.from_orm(query)

            jwt_token = self.sign_jwt(auth_user)
            refresh_jwt = self.sign_refresh(auth_user.id, refresh_token)

            return (jwt_token, refresh_jwt), None

        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    def refresh(self, refresh_token: str):
        try:
            payload, err = self.verify_jwt(refresh_token)
            if err is not None:
                return None, err

            user_id = None
            token = None
            if payload is not None:
                user_id = payload["id"]
                token = payload["refresh_token"].encode("utf-8")

            query = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if query is None:
                return None, DBServiceError(status_code=404, message="user not found")

            match = bcrypt.checkpw(token, query.refresh_token.encode("utf-8"))
            if not match:
                return None, DBServiceError(status_code=400, message="invalid token")

            auth_user = User.from_orm(query)

            jwt_token = self.sign_jwt(auth_user)

            return jwt_token, None
        except Exception as err:
            return None, DBServiceError(status_code=500, message=str(err))

    @staticmethod
    def sign_jwt(user: User) -> str:
        jwt_payload = {
            "id": user.id,
            "username": user.username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        }

        return jwt.encode(jwt_payload, settings().secret_key, algorithm="HS256")

    @staticmethod
    def sign_refresh(user_id: int, refresh_token: str) -> str:
        jwt_payload = {
            "id": user_id,
            "refresh_token": refresh_token,
        }

        return jwt.encode(jwt_payload, settings().secret_key, algorithm="HS256")

    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            return (
                jwt.decode(jwt_token, settings().secret_key, algorithms=["HS256"]),
                None,
            )
        except jwt.ExpiredSignatureError:
            return None, DBServiceError(status_code=401, message="expired token")
        except Exception as err:
            return None, DBServiceError(status_code=401, message=str(err))
