from app import *
from flask_jwt_extended import (jwt_required)


@app.route('/getusers', methods=['GET'])
@jwt_required
def getusers():
    all_users = Mhs.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result), 200


@app.route('/getuser/<id>', methods=['GET'])
@jwt_required
def getuser(id):
    mahasiswa = Mhs.query.get(id)
    return user_schema.jsonify(mahasiswa)


if __name__ == '__main__':
    app.run()
