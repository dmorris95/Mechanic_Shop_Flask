from app.models import Ticket
from app.extensions import ma
from marshmallow import fields

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        fields = ("mechanic_ids", "VIN", "service_date", "service_desc", "customer_id")

class EditTicketSchema(ma.Schema):
    add_ids = fields.List(fields.int(), required=True)
    remove_ids = fields.List(fields.int(), required=True)
    class Meta:
        fields = ("add_ids", "remove_ids")

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()