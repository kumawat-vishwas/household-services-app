from .database import db
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager
from datetime import datetime
import pytz

from werkzeug.security import generate_password_hash, check_password_hash


roles_users = db.Table('roles_users',
            db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
            db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255),unique=True, nullable=False)
    about = db.Column(db.String())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user',lazy='dynamic'))

    
class Role(db.Model, RoleMixin):
    __tablename__ ='role'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),unique = True)
    description = db.Column(db.String(255))

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String)
    address = db.Column(db.String)
    pincode = db.Column(db.Integer)
    status = db.Column(db.String)

class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime(timezone=True),default=datetime.now(pytz.timezone('Asia/Kolkata')))
    # description = db.Column(db.String)
    service_type = db.Column(db.String)
    experience = db.Column(db.Integer)
    address = db.Column(db.String)
    pincode = db.Column(db.Integer)
    document = db.Column(db.String)
    status = db.Column(db.String)

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)
    date_of_request = db.Column(db.DateTime(timezone=True),default=datetime.now(pytz.timezone('Asia/Kolkata')))
    date_of_completion = db.Column(db.String)
    service_status = db.Column(db.String)
    remarks = db.Column(db.String)
    rating = db.Column(db.Integer)

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    time_required = db.Column(db.String)
    description = db.Column(db.String)

class AppProfessionals(db.Model):
    __tablename__ = 'approved_professionals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)

class BlockedCustomers(db.Model):
    __tablename__ = 'blocked_customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class BlockedProfessionals(db.Model):
    __tablename__ = 'blocked_professionals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)

class userVisit(db.Model):
    __tablename__ = 'userVisited'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    professional_id = db.Column(db.Integer,  db.ForeignKey("professional.id"), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),default=datetime.now(pytz.timezone('Asia/Kolkata')))
