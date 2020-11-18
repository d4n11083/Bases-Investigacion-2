from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from pymongo import errors
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

@app.route('/departamentos', methods=['GET'])
def getDepartamentos():
    departamentos = []

    for doc in db.find():
        departamentos.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombreDepartamento': doc['nombreDepartamento']
        })

    return jsonify(departamentos)

@app.route('/departamento', methods=['GET'])
def getDepartamento():
    id = request.json['id']
    departamento = db.find_one({ '_id': ObjectId(id) })

    return jsonify({
        '_id': str(ObjectId(departamento['_id'])),
        'nombreDepartamento': departamento['nombreDepartamento']
    })

@app.route('/departamento', methods=['DELETE'])
def deleteDepartamento():
    id = request.json['id']
    db.delete_one({ '_id' : ObjectId(id) })
    return {'msg': 'Departamento Eliminado'}


@app.route('/departamento', methods=['PUT'])
def updateDepartamento():
    id = request.json['id']
    db.update_one( { '_id': ObjectId(id) }, {'$set':{
        'nombreDepartamento': request.json['nombreDepartamento']
    }})
    return {'msg' : "Departamento Actualizado"}


#Crud Empleados


@app.route('/empleado', methods=['POST'])
def createEmpleado():

    try:
        Departamento = db.find_one({ "nombreDepartamento": request.json["nombreDepartamento"] })['_id']
    except Exception as e:
        return {"Error" : str(e)}
    

    db.update_one( {"_id": ObjectId(Departamento)}, {"$push": {"empleados" : {
        "idEmpleado" : request.json['idEmpleado'],
        "nombreEmpleado" : request.json['nombreEmpleado'],
        "apellidoEmpleado" : request.json['apellidoEmpleado'],
        "fechaIngresoEmpleado" : request.json['fechaIngresoEmpleado'] 
    }}} )
    return jsonify(request.json['idEmpleado'])

@app.route('/empleados', methods=['GET'])
def getEmpleados():
    empleados = []

    for doc in db.find():
        empleados.append({
            "departamento" : doc['nombreDepartamento'],
            "empleados" : doc['empleados'] 
        })

    return jsonify(empleados)

@app.route('/empleado', methods = ['PUT'])
def updateEmpleado():
    idEmpleado = request.json['idEmpleado']

    try:
        Departamento = db.find_one({ "nombreDepartamento": request.json["nombreDepartamento"] })['_id']
    except Exception as e:
        return {"Error" : str(e)}

    db.update_one( {"nombreDepartamento": request.json["nombreDepartamento"], "empleados.idEmpleado":idEmpleado }, { "$set": 
    { "empleados.$.nombreEmpleado":request.json['nuevoNombre'],
     "empleados.$.apellidoEmpleado":request.json['nuevoApellido']  
     }  }  )

    return {"msg" : "Empleado Actualizado"}



@app.route('/empleado', methods = ['DELETE'])
def deleteEmpleado():
    idEmpleado = request.json['idEmpleado']

    try:
        Departamento = db.find_one({ "nombreDepartamento": request.json["nombreDepartamento"] })['_id']
    except Exception as e:
        return {"Error" : str(e)}

    db.update_one( {"_id": ObjectId(Departamento)}, {"$pull": {"empleados" : {
        "idEmpleado" : idEmpleado
    }}} )

    return {"msg" : "Empleado Eliminado"} 

if __name__ == "__main__":
    app.run(debug=True)

