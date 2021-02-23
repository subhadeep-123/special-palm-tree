import gc
import logging
from pymongo import MongoClient, errors
from flask import Flask, render_template

logging.basicConfig(
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(10)
logging.basicConfig(level=10)
app = Flask(__name__)
try:

    client = MongoClient("mongodb://db:27017")  # For Non host network
    # client = MongoClient('localhost', 27017)  # For localhost
    # For Network Mode Host
    # client = MongoClient("mongodb://localhost:27017/db")
except errors.ConnectionFailure as ef:
    logger.exception(ef)
except errors.ServerSelectionTimeoutError as sste:
    logger.exception(sste)
else:
    logger.debug("[CONNECTED TO MONGO CLIENT]")
    db = client.Test
    col = db.one
    logger.debug("[DATABASE CREATED]")


class ToDatabase:
    def __init__(self, name: str, age: int, email: str) -> None:
        self.name = name
        self.age = age
        self.email = email

    def insert_data(self) -> None:
        data = {
            'Name': self.name,
            'Age': self.age,
            'Email': self.email
        }
        data_id = col.insert_one(data).inserted_id
        logger.debug(f'[DATA INSERTED] - object_id - {data_id}')
        gc.collect()

    def exists(self):
        # if col.find({'Email': {"$in": self.email}}).count() > 0: # For If self.email is an array
        if col.find({'Email': self.email, 'Name': self.name}).count() > 0:
            logger.debug(f'[DOCUMENT EXISTS] - {self.email}')
        else:
            logger.debug(f'[DOCUMENT DOES NOT EXISTS] - {self.email}')
            self.insert_data()

    @staticmethod
    def fetch_data_from_db() -> None:
        for data in col.find():
            print(data)

    @staticmethod
    def drop_col() -> None:
        col.drop()
        if 'one' not in db.list_collection_names():
            logger.debug("[SUCESSFULLY DROPPED COLLECTION]")


# Helper Function
def main():
    names = [
        'Subhadeep',
        'Ria',
        'Richard',
        'Soumya',
        'Shubham',
        'Subhadeep',
        'Ria',
        'Richard',
        'Soumya',
        'Shubham',
        'Matrix'
    ]
    ages = [21, 22, 22, 21, 23, 21, 22, 22, 21, 23, 30]
    emails = [
        'subhadeep762@gmail.com',
        'riagupta201@gmail.com',
        'flip.brian35@gmail.com',
        'soumamitra07@gmail.com',
        'shubhamnag789@gmail.com',
        'subhadeep762@gmail.com',
        'riagupta201@gmail.com',
        'flip.brian35@gmail.com',
        'soumamitra07@gmail.com',
        'shubhamnag789@gmail.com',
        'subhadeep@klizos.com'
    ]
    for i in range(len(names)):
        obj = ToDatabase(names[i], ages[i], emails[i])
        obj.exists()
        # obj.insert_data()

    obj.fetch_data_from_db()
    # obj.drop_col()
    # print(db.list_collection_names())


@app.route('/')
def index():
    records = col.find()
    return render_template('index.html', names=records)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # main()
