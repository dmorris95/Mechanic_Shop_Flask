from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", ForeignKey("mechanics.id"))
)

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    password: Mapped[str] = mapped_column(db.String(50), nullable=False)

    tickets: Mapped[List["Ticket"]] = db.relationship(back_populates="customer", cascade="all, delete")

class Ticket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(50), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    customer: Mapped["Customer"] = db.relationship(back_populates="tickets")
    mechanic: Mapped[List["Mechanic"]] = db.relationship(secondary=service_mechanics)

class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    tickets: Mapped[List["Ticket"]] = db.relationship(secondary=service_mechanics)
