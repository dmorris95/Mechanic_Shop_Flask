from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db
from sqlalchemy import select, delete


@inventory_bp.route("/", methods=['POST'])
def create_part():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Inventory(name=part_data['name'], price=part_data['price'])
    
    db.session.add(new_part)
    db.session.commit()

    return inventory_schema.jsonify(new_part), 201

@inventory_bp.route("/", methods=['GET'])
def get_inventory():
    query = select(Inventory)
    result = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(result), 200

@inventory_bp.route("/<int:part_id>", methods=['PUT'])
def update_part(part_id):
    query = select(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query).scalars().first()
    
    if part == None:
        return jsonify({"message": "Invalid part id"})

    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in part_data.items():
        setattr(part, field, value)

    db.session.commit()
    return inventory_schema.jsonify(part), 200


@inventory_bp.route("/<int:part_id>", methods=['DELETE'])
def delete_part(part_id):
    query = delete(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query)

    db.session.commit()
    return jsonify({"message": f"Successfully deleted part {part_id}"})
    
