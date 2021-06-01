from flask_login import UserMixin
from sweater import manager, db


class Admin(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


@manager.user_loader
def load_admin(username):
    user = db.admins.find_one({'username': username})
    return Admin(username=user['username']) if user else None
