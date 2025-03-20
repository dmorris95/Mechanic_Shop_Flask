from app.blueprints.service_tickets import tickets_bp
from app.blueprints.service_tickets.schemas import edit_ticket_schema, ticket_schema, tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Ticket, Mechanic, db
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

    return ticket_schema.jsonify(new_ticket)

@tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_tickets():
    query = select(Ticket)
    result = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(result), 200

@tickets_bp.route("/<int:ticket_id>", methods=['DELETE'])
@limiter.limit("3 per hour")
def delete_ticket(ticket_id):
    query = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted service ticket with ID: {ticket_id}"})

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

        if ticket and ticket not in ticket.mechanic:
            ticket.mechanic.append(mechanic)

    for mechanic_id in ticket_edit['remove_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if ticket and ticket in ticket.mechanic:
            ticket.mechanic.remove(mechanic)
    
    db.session.commit()
    return ticket_schema.jsonify(ticket)
