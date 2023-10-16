import random

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from flask_smorest import abort

import models
from schemas import RegisterSchema, PlainUserSchema, VerifySchema
from db import db

blp = Blueprint('Users', __name__, description='Operations on users')


@blp.route('/register')
class User(MethodView):
    @blp.response(200, "Success")
    @blp.arguments(RegisterSchema)
    def post(self, data):
        random_number = random.randint(100000, 999999)
        user = models.UserModel(
            username=data['username'],
            email=data['email'],
            password=pbkdf2_sha256.hash(data["password"]),
            verified=str(random_number)
        )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))

        return jsonify({'message': 'User created successfully.'}), 200


@blp.route('/login')
class Login(MethodView):
    @blp.response(200, PlainUserSchema)
    @blp.arguments(PlainUserSchema)
    def post(self, data):
        user = (db.session.execute(db.select(models.UserModel).where(models.UserModel.email == data['email']))
                .scalar_one_or_none())
        if not user:
            abort(400, message="User not found.")
        if not pbkdf2_sha256.verify(data["password"], user.password):
            abort(400, message="Invalid password.")

        if user.verified is None:
            return jsonify({'message': 'User logged in successfully.'}), 200
        else:
            abort(400, message="User not verifed.")


@blp.route('/verify')
class Verify(MethodView):
    @blp.response(200, VerifySchema)
    @blp.arguments(VerifySchema)
    def post(self, data):
        user = (db.session.execute(db.select(models.UserModel).where(models.UserModel.email == data['email']))
                .scalar_one_or_none())
        if not user:
            abort(400, message="User not found.")
        if not pbkdf2_sha256.verify(data["password"], user.password):
            abort(400, message="Invalid password.")
        if user.verified != data['verified']:
            abort(400, message="Invalid verification code.")
        user.verified = None
        try:
            db.session.commit()
        except Exception as e:
            abort(500, message=str(e))
        return jsonify({'message': 'User verified successfully.'}), 200
