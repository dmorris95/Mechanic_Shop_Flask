from app.blueprints.service_tickets import tickets_bp
from app.blueprints.service_tickets.schemas import edit_ticket_schema, ticket_schema, tickets_schema, part_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Ticket, Mechanic, Inventory, db
from sqlalchemy import select
from app.extensions import limiter, cache

@tickets_bp.route("/", methods=['POST'])
@limiter.limit("20 per hour")
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = Ticket(VIN=ticket_data['VIN'], service_date=ticket_data['service_date'], service_desc=ticket_data['service_desc'], customer_id=ticket_data['customer_id'])

    for mechanic_id in ticket_data['mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_ticket.mechanic.append(mechanic)
        else:
            return jsonify({"message": "Invalid mechanic id"})

    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 201

@tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_tickets():
    query = select(Ticket)
    result = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(result), 200

@tickets_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket(ticket_id):
    try:
        ticket_edit = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    for mechanic_id in ticket_edit['add_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if ticket and mechanic not in ticket.mechanic:
            ticket.mechanic.append(mechanic)

    for mechanic_id in ticket_edit['remove_ids']:
        print(mechanic_id)
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if ticket and mechanic in ticket.mechanic:
            ticket.mechanic.remove(mechanic)
    
    db.session.commit()
    return ticket_schema.jsonify(ticket)

@tickets_bp.route('/<int:ticket_id>/add-part', methods=['PUT'])
def add_part_ticket(ticket_id):
    try:
        ticket_edit = part_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()
    
    for part_id in ticket_edit['add_ids']:
        query = select(Inventory).where(Inventory.id == part_id)
        part = db.session.execute(query).scalars().first()
        if part:
            if ticket:
                ticket.parts.append(part)
        else:
            return jsonify({"message": "Invalid Part ID"})

    db.session.commit()
    print(ticket.parts)
    return ticket_schema.jsonify(ticket)