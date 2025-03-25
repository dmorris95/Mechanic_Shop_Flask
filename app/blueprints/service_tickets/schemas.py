from app.models import Ticket
from app.extensions import ma
from marshmallow import fields

class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic = fields.Nested("MechanicSchema", many=True)
    parts = fields.Nested("InventorySchema", many=True)
    class Meta:
        model = Ticket
        fields = ("mechanic_ids", "VIN", "service_date", "service_desc", "customer_id", "mechanic", "parts")

class EditTicketSchema(ma.Schema):
    add_ids = fields.List(fields.Int(), required=True)
    remove_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_ids", "remove_ids")

class AddPartTcketSchema(ma.Schema):
    add_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_ids",)

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()
part_ticket_schema = AddPartTcketSchema()