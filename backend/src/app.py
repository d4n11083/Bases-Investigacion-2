from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/Investigacion2'
mongo = PyMongo(app)


CORS(app)

db = mongo.db.departamentos


@app.route('/departamento', methods=['POST'])
def createDepartamento():
    id = db.insert({
        'nombreDepartamento': request.json['nombreDepartamento'],
        'empleados' : []
    })

    return jsonify(str(ObjectId(id)))

@app.route('/departamento', methods=['GET'])
def getDepartamentos():
    departamentos = []

    for doc in db.find():
        departamentos.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombreDepartamento': doc['nombreDepartamento']
        })

    return jsonify(users)

@app.route('/departamento/<id>', methods=['GET'])
def getDepartamento(id):
    departamento = db.find_one({ '_id': ObjectId(id) })

    return jsonify({
        '_id': str(ObjectId(departamento['_id'])),
        'nombreDepartamento': departamento['name']
    })

@app.route('/departamento/<id>', methods=['DELETE'])
def deleteDepartamento(id):

    db.delete_one({ '_id' : ObjectId(id) })
    return {'msg': 'Departamento Eliminado'}


@app.route('/departamento/<id>', methods=['PUT'])
def updateDepartamento(id):
    db.update_one( { '_id': ObjectId(id) }, {'$set':{
        'nombreDepartamento': request.json['nombreDepartamento']
    }
    } )

    return {'msg' : "user Updated"}

if __name__ == "__main__":
    app.run(debug=True)

