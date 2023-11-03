from werkzeug.security import safe_str_cmp
from models.user import UserModel


# from User import User


def authentication(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_ID(user_id)
