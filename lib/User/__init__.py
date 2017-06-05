from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "{0}:{1}".format(self.id, self.username)

    def __str__(self):
        return self.username