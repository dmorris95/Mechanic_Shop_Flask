from app.models import Ticket
from app.extensions import ma

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        fields = ("mechanic_ids", "VIN", "service_date", "service_desc", "customer_id")

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)