from app.blueprints.service_tickets import tickets_bp
from app.blueprints.service_tickets.schemas import ticket_schema, tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Ticket, Mechanic, db
from sqlalchemy import select

@tickets_bp.route("/", methods=['POST'])
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
def get_tickets():
    query = select(Ticket)
    result = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(result), 200