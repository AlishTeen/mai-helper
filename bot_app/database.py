import pymongo as pm
from pymongo import errors
from datetime import datetime

from bot_app.models import User


class DataBaseClass:
    def __init__(self, login, password, host):
        self.client = pm.MongoClient(f'mongodb+srv://{login}:{password}@{host}/?retryWrites=true&w=majority')
        self.db = self.client['bot_db']
        self.users_col = self.db['users']
        self.questions_col = self.db['questions']
        self.autoinc = self.db['autoinc']
        self.stat_col = self.db['stat']

    def get_user(self, user_id):
        res = self.users_col.find_one({'user_id': user_id}, {'_id': 0})
        return User(**res) if res else False

    def add_user(self, user: User):
        try:
            user.register_time = datetime.utcnow()
            res = self.users_col.insert_one(user.__dict__)
            return True if res.inserted_id else False
        except errors.OperationFailure:
            return False

    def user_exists(self, user_id):
        return self.users_col.find_one({'user_id': user_id}) is not None

    def edit_user(self, user_id, user_obj: User = None, **kwargs):
        if user_obj:
            res = self.users_col.update_one({'user_id': user_obj.user_id},
                                            {'$set': user_obj.__dict__})
        else:
            res = self.users_col.update_one({'user_id': user_id},
                                            {'$set': kwargs})
        return res.modified_count != 0

    def delete_user(self, user_id):
        res = self.users_col.delete_one({'user_id': user_id})
        self.questions_col.delete_many({'user_id': user_id})
        return res.deleted_count != 0

    def add_question(self, user_id, text):
        res = self.questions_col.insert_one({'_id': self.get_unique_id(),
                                             'user_id': user_id,
                                             'text': text,
                                             'datetime': datetime.utcnow(),
                                             'answered': False,
                                             'answer': None})
        return res.inserted_id if res.inserted_id else False

    def get_unique_id(self):
        res = self.autoinc.find_one_and_update({'_id': 'lastQuestionCounter'},
                                               {'$inc': {'counter': 1}},
                                               upsert=True)
        return int(res['counter'])

    def stat_dialogflow_inc(self):
        res = self.autoinc.update_one({'_id': 'dflow_count'}, {'$inc': {'counter': 1}})
        return res.modified_count
