from flask_restful import Resource, reqparse
from .user_service import UsersService


class Base():
    __service__ = UsersService

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='Inform an email'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Inform a password'
    )


class UserCreation(Resource, Base):
    def post(self):
        data = UserCreation.parser.parse_args()
        return self.__service__.add_user(self, **data)


class UserLogin(Resource, Base):
    def post(self):
        data = UserCreation.parser.parse_args()
        return self.__service__.login(self, **data)
