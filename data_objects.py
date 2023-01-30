import pymongo


def update_data(collection, data, new_values):  # update data in mongodb
    collection.update_one(data, {'$set': new_values})


def insert_data(collection, data):  # for data inserting to mongodb
    return collection.insert_one(data).inserted_id


def find_data(collection, data):  # serching data in mongodb
    return collection.find_one(data)


mongoCl = pymongo.MongoClient('localhost')
db = mongoCl['jbot']
users = db['users']


class User:

    def __init__(self, discord_id: int):

        user = find_data(users, {'id': discord_id})

        if user is None:
            insert_data(users, {'id': discord_id, 'tr_lang': '', 'b_w': 0})
            self.user = {'id': discord_id, 'tr_lang': '', 'b_w': 0}

        else:
            self.user = user

    def update(self, data):

        update_data(users, {'id': self.user['id']}, data)
        self.user = find_data(users, {'id': self.user['id']})
