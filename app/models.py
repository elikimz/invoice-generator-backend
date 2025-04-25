import uuid
import enum
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey,
    Float, Integer, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base

# ==================== Enums ====================
class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class SubscriptionStatus(str, enum.Enum):
    pending = "pending"
    active = "active"
    expired = "expired"
    failed = "failed"

# ==================== User ====================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_google_user = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoices = relationship("Invoice", back_populates="user", cascade="all, delete")
    clients = relationship("Client", back_populates="user", cascade="all, delete")
    settings = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete")

# ==================== Client ====================
class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)
    company_name = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="clients")
    invoices = relationship("Invoice", back_populates="client", cascade="all, delete")

# ==================== Invoice ====================
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"))
    invoice_number = Column(String, nullable=False, unique=True)
    due_date = Column(DateTime)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    total_amount = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="invoices")
    client = relationship("Client", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete")

# ==================== Invoice Item ====================
class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")

# ==================== Payment ====================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    paid_at = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="payments")

# ==================== Settings ====================
class Settings(Base):
    __tablename__ = "settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    currency = Column(String, default="USD")
    business_name = Column(String)
    logo_url = Column(String)
    default_terms = Column(String)

    user = relationship("User", back_populates="settings")

# ==================== Subscriptions ====================
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.pending)
    plan_name = Column(String, default="Basic")  # "Basic", "Pro", etc.
    payment_method = Column(String, default="stripe")  # or "mpesa"
    payment_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)

    user = relationship("User", back_populates="subscriptions")
