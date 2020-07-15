from flask_restful import Resource, Api
from flask import Flask, Response, request, json, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)



class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True)
    nama = db.Column(db.String(20))
    alamat= db.Column(db.String(20))

    def __init__(self, nim, nama, alamat):
        self.nim = nim
        self.nama = nama
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mahasiswa.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'nama', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/mahasiswa/', methods=['POST'])
def add_user():
    nim = request.json['nim']
    nama = request.json['nama']
    alamat = request.json['alamat']

    new_mhs = Mahasiswa(nim, nama, alamat)

    db.session.add(new_mhs)
    db.session.commit()

    return user_schema.jsonify(new_mhs)

@app.route('/mahasiswa/', methods=['GET'])
def get_users():
    all_users = Mahasiswa.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/mahasiswa/<id>', methods=['GET'])
def get_user(id):
  mahasiswa = Mahasiswa.query.get(id)
  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<id>', methods=['PUT'])
def update_user(id):
  mahasiswa = Mahasiswa.query.get(id)

  nim = request.json['nim']
  nama = request.json['nama']
  alamat = request.json['alamat']

  mahasiswa.nim = nim
  mahasiswa.nama = nama
  mahasiswa.alamat = alamat

  db.session.commit()

  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<id>', methods=['DELETE'])
def delete_product(id):
  mahasiswa = Mahasiswa.query.get(id)
  db.session.delete(mahasiswa)
  db.session.commit()

  return user_schema.jsonify(mahasiswa)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400



    nama = request.json.get('nama', None)
    password = request.json.get('password', None)

    login_user = Mhs.query.filter_by(nama=nama).first()
    print(login_user.nama)
    print(login_user.password)
    # print(nama)
    if not nama:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if nama != login_user.nama or password != login_user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=nama)
    return jsonify(access_token=access_token), 200

@app.route('/getUser', methods=['GET'])
@jwt_required
def getuser():
    all_users = Mhs.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result), 200
    # return jsonify(Mhs.query.all()), 200


if __name__ == '__main__':
    app.run()
