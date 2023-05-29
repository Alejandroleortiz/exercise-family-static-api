"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    
    if not members: # this checks if the list is empty
        return jsonify({"msg":"No members found"}), 404

    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member_by_id(id):
    member = jackson_family.get_member(id)
    
    if member:
        return jsonify( member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404
    

@app.route('/member', methods=['POST'])
def add_member():
    member = request.get_json()
    required_fields = ["first_name", "age", "lucky_numbers"]
    
    if not all(field in member for field in required_fields):
            return jsonify({"msg": "Missing required field"}), 400
        
    jackson_family.add_member(member)
    
    return member, 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member_deleted = jackson_family.delete_member(id)
    
    if member_deleted:
        return jsonify({"done": member_deleted}), 200
    else:
        return jsonify({"done": 'Member did not delete'}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
