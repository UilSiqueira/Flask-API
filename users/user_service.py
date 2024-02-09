from flask_restful import reqparse
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from .model import UsersModel
from .exceptions import UserAlreadyExistsException, UserEmailOrPasswordInvalidException
from db import db


class UsersService:
    def add_user(self, kwargs: reqparse.Namespace):
        user = UsersModel. query.filter_by(email=kwargs['email']).first()
        if user:
            raise UserAlreadyExistsException(
                'There is already a user with this Email {}'.format(kwargs['email']))

        new_user = UsersModel(**kwargs)
        db.session.add(self)
        db.session.commit()

        return new_user.as_dict()

    def login(self, kwargs: reqparse.Namespace):
        user = UsersModel. query.filter_by(email=kwargs['email']).first()
        if user and pbkdf2_sha256.verify(kwargs['password'], user.password):
            token = create_access_token(identity=user.id)
            return {'access_token': token}

        raise UserEmailOrPasswordInvalidException(
            'User or password not valid')
