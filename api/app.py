#!/usr/bin/python

from flask import Flask, jsonify, request, json
from heyu import heyu, Status

# ------------------------------------------------
# Instanciate the flask application
# ------------------------------------------------

app = Flask(__name__)

# ------------------------------------------------
# Define the JSON encoder that supports objects
# ------------------------------------------------

class ObjJSONEncoder(json.JSONEncoder):        
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        return super(ObjJSONEncoder, self).default(obj)

app.json_encoder = ObjJSONEncoder
app.url_map.strict_slashes = False

# ------------------------------------------------
# Define the routes
# ------------------------------------------------

@app.route('/api/', methods=['GET'])
def index():
    return jsonify('/api/settings', '/api/aliases', '/api/macros', '/api/schedules', '/api/commands', '/api/units')

@app.route('/api/status/', methods=['GET'])
def getStatus():
    return jsonify(heyu.getStatus())

# Settings
@app.route('/api/settings/', methods=['GET'])
def getSettings():
    return jsonify(heyu.getSettings())

@app.route('/api/settings/<id>', methods=['GET'])
def getSetting(id):
    return jsonify(heyu.getSetting(id))

@app.route('/api/settings/<id>', methods=['POST'])
def postSetting(id):
    return jsonify(heyu.upsertSetting(id, request.json))

# Aliases
@app.route('/api/aliases/', methods=['GET'])
def getAliases():
    return jsonify(heyu.getAliases())

@app.route('/api/aliases/<id>', methods=['GET'])
def getAlias(id):
    return jsonify(heyu.getAlias(id))

@app.route('/api/aliases/<id>', methods=['POST'])
def postAlias(id):
    return jsonify(heyu.upsertAlias(id, request.json))

@app.route('/api/aliases/<id>', methods=['DELETE'])
def deleteAlias(id):
    return jsonify(heyu.deleteAlias(id))

# Macros
@app.route('/api/macros/', methods=['GET'])
def getMacros():
    return jsonify(heyu.getMacros())

@app.route('/api/macros/<id>', methods=['GET'])
def getMacro(id):
    return jsonify(heyu.getMacro(id))

@app.route('/api/macros/<id>', methods=['POST'])
def postMacro(id):
    return jsonify(heyu.upsertMacro(id, request.json))

@app.route('/api/macros/<id>', methods=['DELETE'])
def deleteMacro(id):
    return jsonify(heyu.deleteMacro(id))

# Schedules
@app.route('/api/schedules/', methods=['GET'])
def getSchedules():
    if request.args.get('file','false') == "true":
        return jsonify(heyu.getSchedulesFile())
    return jsonify(heyu.getSchedules())

@app.route('/api/schedules/<id>', methods=['GET'])
def getSchedule(id):
    return jsonify(heyu.getSchedule(id))

@app.route('/api/schedules/<id>', methods=['POST'])
def postSchedule(id):
    return jsonify(heyu.upsertSchedule(id, request.json))

@app.route('/api/schedules/<id>', methods=['DELETE'])
def deleteSchedule(id):
    return jsonify(heyu.deleteSchedule(id))

# Units
@app.route('/api/units/', methods=['GET'])
def getUnits():
    return jsonify(heyu.getUnits(request.args.get('housecode', '')))

@app.route('/api/units/<id>', methods=['GET'])
def getUnit(id):
    return jsonify(heyu.getUnit(id))

@app.route('/api/units/<id>', methods=['POST'])
def postUnit(id):
    return jsonify(heyu.setUnitStatus(id, request.json))

@app.route('/api/units/<id>', methods=['PATCH'])
def patchUnit(id):
    return jsonify(heyu.setUnitModule(id))

# Commands
@app.route('/api/commands/', methods=['GET'])
def getCommands():
    return jsonify(heyu.getCommands())

@app.route('/api/commands/', methods=['POST'])
def postCommands():
    return jsonify(heyu.execCommand(request.json["cmd"]))

if __name__ == '__main__':
    # Will make the server available externally as well
    #app.debug = True
    app.run(host='0.0.0.0')
