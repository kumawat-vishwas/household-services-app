from flask_restful import Resource
from flask import Response
import os
import pytz
import json

from datetime import datetime
from datetime import datetime as date, timedelta


from flask_restful import fields, marshal_with
from flask_restful import reqparse

from application.database import db
from application.models import User, Customer, Professional,Role,ServiceRequest, Services, userVisit
from application import tasks
from application.validation import NotFoundError, BusinessValidationError
import matplotlib.pyplot as plt
from io import BytesIO
from application.cache import cache


import flask_login
import flask_security
from flask_security import auth_required, login_required, roles_accepted, roles_required,auth_token_required,current_user,logout_user

from flask import request, jsonify
from flask_security import login_user, current_user



album_data = {
    "id": fields.Integer,
    "name":fields.String,
    "date_created":fields.String,
}

album_parser =  reqparse.RequestParser()
album_parser.add_argument('name')
album_parser.add_argument('newName')


class clearCache(Resource):
    def post(self):
        cache.delete('allServicesbyUser_cache')
        cache.delete('getServiceDetails_cache')
        return "Cache Cleared",200

class checkUserPermission(Resource):
    @auth_required('token')
    def get(self):
        user = flask_login.current_user
        if user.roles:
            if user.roles[0]:
                if user.roles[0].name == 'admin':
                    return "Admin",200
                elif user.roles[0].name == 'professional':
                    return "Professional",200
                elif user.roles[0].name == 'customer':
                    return "Customer",200
        return "No role associated with this user",404
    
class checkUserBlockedStatus(Resource):
    @auth_required('token')
    def get(self):
        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        if customer:
            if customer.status == 'blocked':
                return "Blocked",200
            return "Customer is not blocked",200
        return "Customer not found",404

class userTypeAPI(Resource):
    def get(self,email):

        user = User.query.filter_by(email=email).first()
        if user:
            try:
                acc_type = user.roles[0].name
                if acc_type:
                    if acc_type == 'customer':
                        return {"type":"customer"},200
                    elif acc_type == 'professional':
                        return {"type":"professional"},200
                    elif acc_type == 'admin':
                        return {"type":"admin"},200
            except Exception as e:
                return "No role associated with this user",200
            
        else:
            return "User Not Found",404

class registerCustomerDetails(Resource):
    @auth_required("token")
    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            address = data.get('address')
            pincode = data.get('pincode')
            user = flask_login.current_user
            customer_email_already = Customer.query.filter_by(user_id=user.id).first()
            if customer_email_already:
                customer_email_already.name = name
                customer_email_already.address = address
                customer_email_already.pincode = pincode
            else:
                new_customer = Customer(user_id=user.id,name=name,address=address,pincode=pincode,status= 'unblocked')
                db.session.add(new_customer)
                db.session.commit()
            return "Customer Details Updated Successfully",201
        except Exception as e:
            return "An error occured",500

class registerProfessionalDetails(Resource):
    @auth_required("token")
    def post(self):
        try:
            email = request.form['email']
            name = request.form['name']
            address = request.form['address']
            pincode = request.form['pincode']
            selectedService = request.form['selectedService']
            experience = request.form['experience']
            acc_type = request.form['type']
            file = request.files['file']
            user = flask_login.current_user

            if len(email)<=0:
                return "Email required", 400
            if len(name)<=0:
                return "Name required", 400
            if len(address)<=0:
                return "Address required", 400
            if len(pincode)<=0:
                return "Pincode required", 400
            if len(selectedService)<=0:
                return "Service required", 400
            if len(experience)<=0:
                return "Experience required", 400
            if len(acc_type)<=0:
                return "Account type required", 400
            if file.filename == '':
                return "No files selected. Upload it.",400
            
            professional_email_already = Professional.query.filter_by(user_id=user.id).first()

            if file and file.filename.endswith('.pdf'):
                file.save(os.path.join('static/pdf', file.filename))

            if professional_email_already:
                professional_email_already.name = name
                professional_email_already.address = address
                professional_email_already.pincode = pincode
                professional_email_already.service_type = selectedService
                professional_email_already.experience = experience
                professional_email_already.document = file.filename
            else:
                new_professional = Professional(user_id=user.id,name=name,address=address,pincode=pincode,service_type=selectedService,experience=experience,document = file.filename)
                db.session.add(new_professional)
                db.session.commit()

            return "Service Professional Details Updated Successfully",201
        except Exception as e:
            return "An error occured",500
        
class addUserRole(Resource):
    @auth_required("token")
    def post(self):
        user = flask_login.current_user
        data = request.get_json()
        if data:
            role = data
            if role == 'customer':
                user.roles.append(Role.query.filter_by(name='customer').first())
            elif role == 'professional':
                user.roles.append(Role.query.filter_by(name='professional').first())
            elif role == 'admin':
                user.roles.append(Role.query.filter_by(name='admin').first())
            db.session.commit()
            return "Role added successfully",201


class getAllServiceTypesName(Resource):
    @auth_required("token")
    def get(self):
        services = Services.query.all()
        all_services = set()
        if services:
            for service in services:
                all_services.add(service.name)
        return {"services":list(all_services)}, 200
  


class getAllTodayServices(Resource):
    @auth_required("token")
    def get(self):
        user  = flask_login.current_user
        if user.roles:
            if user.roles[0]:
                if user.roles[0].name == 'professional':
                    professional = Professional.query.filter_by(user_id=user.id).first()
                    service_request = ServiceRequest.query.filter_by(professional_id=professional.id,service_status='requested').all()
                    all_services = []
                    for service in service_request:
                        dict = {}
                        customer = Customer.query.filter_by(id=service.customer_id).first()
                        dict['service_request_id'] = service.id
                        dict['customer_name'] = customer.name
                        dict['customer_address'] = customer.address
                        dict['customer_pincode'] = customer.pincode
                        dict['date_of_request'] = service.date_of_request.strftime('%Y-%m-%d %H:%M:%S')
                        dict['service_status'] = service.service_status
                        all_services.append(dict)
                    return all_services, 200
        return "An error occurred",404

  

class getAllClosedServices(Resource):
    @auth_required("token")
    def get(self):
        user  = flask_login.current_user
        if user.roles:
            if user.roles[0]:
                if user.roles[0].name == 'professional':
                    professional = Professional.query.filter_by(user_id=user.id).first()
                    service_request = ServiceRequest.query.filter_by(professional_id=professional.id,service_status='closed').all()
                    all_closed_services = []
                    for service in service_request:
                        dict = {}
                        customer = Customer.query.filter_by(id=service.customer_id).first()
                        dict['service_request_id'] = service.id
                        dict['customer_name'] = customer.name
                        dict['customer_address'] = customer.address
                        dict['customer_pincode'] = customer.pincode
                        dict['date_of_request'] = service.date_of_request.strftime('%Y-%m-%d %H:%M:%S')
                        dict['date_of_completion'] = service.date_of_completion
                        dict['rating'] = service.rating
                        dict['remarks'] = None
                        if service.remarks:
                            dict['remarks'] = service.remarks
                        all_closed_services.append(dict)
                    return all_closed_services, 200
        return "An error occurred",404

  

class getServiceDetails(Resource):
    @auth_required("token")
    @cache.cached(timeout=20, key_prefix='getServiceDetails_cache')
    def get(self,name):
        services = Services.query.filter_by(name=name).first()
        professionals = Professional.query.filter_by(service_type=name).all()
        all_professionals = []
        for professional in professionals:
            if professional.status!='blocked':
                dict = {}
                user = flask_login.current_user
                customer = Customer.query.filter_by(user_id=user.id).first()
                service_request_already = ServiceRequest.query.filter_by(professional_id=professional.id,customer_id=customer.id).first()
                
                dict['service_status'] = None
                dict['service_request_id'] = None
                if service_request_already:
                    dict['service_status'] = service_request_already.service_status
                    dict['service_request_id'] = service_request_already.id
                dict['name'] = professional.name
                dict['address'] = professional.address
                dict['experience'] = professional.experience
                dict['pincode'] = professional.pincode
                dict['document'] = professional.document
                dict['id'] = professional.id
                dict['date_created'] = professional.date_created.strftime('%Y-%m-%d %H:%M:%S')
                all_professionals.append(dict)
        return {"service":services.name,"price":services.price,"time_required":services.time_required,"description":services.description,"professionals":all_professionals}, 200
    
   
class acceptServiceRequest(Resource):
    @auth_required('token')
    def post(self):
        try:
            data = request.get_json()
            service_request_id = data.get('service_request_id')
            user = flask_login.current_user
            professional = Professional.query.filter_by(user_id=user.id).first()
            service_request = ServiceRequest.query.filter_by(id=service_request_id,professional_id=professional.id).first()
            if service_request:
                service_request.service_status = 'assigned'
                db.session.commit()
                return "Service Request Accepted Successfully",201
            return "Service Request not found",404
        except Exception as e:
            return "An error occured",500
        
class rejectServiceRequest(Resource):
    @auth_required('token')
    def post(self):
        try:
            data = request.get_json()
            service_request_id = data.get('service_request_id')
            user = flask_login.current_user
            professional = Professional.query.filter_by(user_id=user.id).first()
            service_request = ServiceRequest.query.filter_by(id=service_request_id,professional_id=professional.id).first()
            if service_request:
                service_request.service_status = 'rejected'
                db.session.commit()
                return "Service Request rejected Successfully",201
            return "Service Request not found",404
        except Exception as e:
            return "An error occured",500
    
class bookProfessional(Resource):
    @auth_required('token')
    def post(self):
        try:
            data = request.get_json()
            professional_id = data.get('professional_id')

            professional_relation = Professional.query.filter_by(id=professional_id).first()
            if not professional_relation:
                return "Professional not found",404
            
            service_relation = Services.query.filter_by(name=professional_relation.service_type).first()
            if not service_relation:
                return "Service not found",404
            
            user = flask_login.current_user

            customer = Customer.query.filter_by(user_id=user.id).first()

            service_request = ServiceRequest.query.filter_by(professional_id=professional_id,customer_id=customer.id,service_id=service_relation.id).first()

            if service_request:
                return "Service already requested",409
            
            new_service_request = ServiceRequest(professional_id=professional_id,customer_id=customer.id,service_id=service_relation.id,service_status='requested')
            db.session.add(new_service_request)
            db.session.commit()
            return "Service Requested Successfully",201
        except Exception as e:
            return "An error occured",500
    
class closeServiceBooking(Resource):
    @auth_required('token')
    def post(self):
        try:
            data = request.get_json()
            service_request_id = data.get('service_request_id')
            ratingDict = data.get('ratingDict')
            
            user = flask_login.current_user
            customer = Customer.query.filter_by(user_id=user.id).first()
            service_request = ServiceRequest.query.filter_by(id=service_request_id,customer_id=customer.id).first()

            if service_request is None:
                return "Service is not requested",409
            
            if service_request.service_status == 'assigned':
                service_request.service_status = 'closed'
                service_request.rating = ratingDict['rating']
                service_request.remarks = ratingDict['remarks']
                service_request.date_of_completion = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

            db.session.commit()
            return "Service Closed Successfully",201
        except Exception as e:
            return "An error occured",500

class deleteServiceHistoryCustomer(Resource):
    @auth_required('token')
    def delete(self,service_request_id):
        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        service_request = ServiceRequest.query.filter_by(id=service_request_id,customer_id=customer.id).first()
        if service_request:
            db.session.delete(service_request)
            db.session.commit()
            return "Service Deleted Successfully",200
        return "Service not found",404

class updateServiceHistoryCustomer(Resource):
    @auth_required('token')
    def put(self):
        data = request.get_json()
        service_request_id = data.get('id')
        date_of_request = data.get('date_of_request')

        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        service_request = ServiceRequest.query.filter_by(id=service_request_id,customer_id=customer.id).first()
        if service_request:
            service_request.date_of_request = datetime.strptime(date_of_request, '%Y-%m-%d')
            db.session.commit()
            return "Service Updated Successfully",201
        return "Service not found",404
    
class updateUserData(Resource):
    @auth_required('token')
    def put(self):
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        pincode = data.get('pincode')
        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        if customer:
            customer.name = name
            customer.address = address
            customer.pincode = pincode
            db.session.commit()
            return "User Updated Successfully",201
        return "User not found",404

class getAccpetedRejected(Resource):
    @auth_required('token')
    def get(self):
        user = flask_login.current_user
        professional = Professional.query.filter_by(user_id=user.id).first()
        service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
        all_services = []
        for service_request in service_requests:
            if service_request.service_status == 'assigned' or service_request.service_status == 'rejected':
                dict = {}
                customer = Customer.query.filter_by(id=service_request.customer_id).first()
                service = Services.query.filter_by(id=service_request.service_id).first()
                dict['service_id'] = service_request.id
                dict['service_name'] = service.name
                dict['customer_name'] = customer.name
                dict['customer_address'] = customer.address
                dict['customer_pincode'] = customer.pincode
                dict['date_of_request'] = service_request.date_of_request.strftime('%Y-%m-%d %H:%M:%S')
                dict['date_of_completion'] = service_request.date_of_completion
                dict['remarks'] = service_request.remarks
                dict['rating'] = service_request.rating
                dict['service_status'] = service_request.service_status
                all_services.append(dict)
        return all_services,200
    
class allServicesbyUser(Resource):
    @auth_required('token')
    @cache.cached(timeout=20, key_prefix='allServicesbyUser_cache')
    def get(self):
        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        service_requests = ServiceRequest.query.filter_by(customer_id=customer.id).all()
        all_services = []
        for service_request in service_requests:
            dict = {}
            professional = Professional.query.filter_by(id=service_request.professional_id).first()

            service = Services.query.filter_by(id=service_request.service_id).first()

            if service_request.service_status == 'assigned' or service_request.service_status == 'requested' or service_request.service_status == 'closed':
                dict['service_request_id'] = service_request.id
                dict['service_status'] = service_request.service_status
                dict['service_name'] = service.name
                dict['service_price'] = service.price
                dict['service_time_required'] = service.time_required
                dict['service_description'] = service.description
                dict['name'] = professional.name
                dict['address'] = professional.address
                dict['experience'] = professional.experience
                dict['pincode'] = professional.pincode
                dict['document'] = professional.document
                dict['id'] = professional.id
                dict['date_created'] = professional.date_created.strftime('%Y-%m-%d %H:%M:%S')
                dict['date_of_request'] = service_request.date_of_request.strftime('%Y-%m-%d %H:%M:%S')
                dict['date_of_completion'] = service_request.date_of_completion
                dict['rating'] = service_request.rating
                dict['remarks'] = service_request.remarks
                all_services.append(dict)
        return all_services,200


class userProfile(Resource):
    @auth_required("token")
    def get(self):
        user = flask_login.current_user
        if user.roles[0]:
            if user.roles[0].name == 'customer':
                customer = Customer.query.filter_by(user_id=user.id).first()
                data = {'email':user.email,'name':customer.name,'address':customer.address,'pincode':customer.pincode}
                return data,200
            else:
                return "You are not customer",400
        else:
            return "An error occurred",500
        


class professionalProfile(Resource):
    @auth_required("token")
    def get(self):
        user = flask_login.current_user
        if user.roles[0]:
            if user.roles[0].name == 'professional':
                professional = Professional.query.filter_by(user_id=user.id).first()
                data = {'email':user.email,'name':professional.name,'address':professional.address,'pincode':professional.pincode,'service_type':professional.service_type,'experience':professional.experience,'document':professional.document,'date_created':professional.date_created.strftime('%d-%m-%Y %H:%M:%S')}
                return data,200
            else:
                return "You are not professional",400
        else:
            return "An error occurred",500
        
class ServicesAPI(Resource):
    @auth_required('token')
    def get(self):
        services = Services.query.all()
        all_services = []
        for service in services:
            dict = {}
            dict['id'] = service.id
            dict['name'] = service.name
            dict['price'] = service.price
            dict['time_required'] = service.time_required
            dict['description'] = service.description
            all_services.append(dict)
        return all_services,200    

    @auth_required('token')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        time_required = data.get('time_required')
        description = data.get('description')
        if not name:
            return "Name is required",400
        if not price:
            return "Price is required",400
        if not time_required:
            return "Time required is required",400
        if not description:
            return "Description is required",400
        service_already = Services.query.filter_by(name=name).first()
        if service_already:
            return "Service already exists",409
        new_service = Services(name=name,price=price,time_required=time_required,description=description)
        db.session.add(new_service)
        db.session.commit()
        return "Service Added Successfully",201 
    
    @auth_required('token')
    def put(self):
        data = request.get_json()
        service_id = data.get('id')
        name = data.get('name')
        price = data.get('price')
        time_required = data.get('time_required')
        description = data.get('description')
        if not name:
            return "Name is required",400
        if not price:
            return "Price is required",400
        if not time_required:
            return "Time required is required",400
        if not description:
            return "Description is required",400
        service_already = Services.query.filter_by(id=service_id).first()
        if not service_already:
            return "Service does not exist",404
        service_already.name = name
        service_already.price = price
        service_already.time_required = time_required
        service_already.description = description
        db.session.commit()
        return "Service Updated Successfully",201
    
    @auth_required('token')
    def delete(self,service_id):
        service_already = Services.query.filter_by(id=service_id).first()
        if not service_already:
            return "Service does not exist",404
        service_request = ServiceRequest.query.filter_by(service_id=service_id).all()
        if service_request:
            return "Service can't be deleted as it is already requested by some customers",409
        db.session.delete(service_already)
        db.session.commit()
        return "Service Deleted Successfully",200

class getServicesAvailable(Resource):
    def get(self):
        all_services = []
        services = Services.query.all()
        for service in services:
            all_services.append(service.name)
        return all_services,200

class professionalAPI(Resource):
    @auth_required('token')
    def get(self):
        professionals = Professional.query.all()
        all_professionals = []
        for professional in professionals:
            dict = {} 
            dict['id'] = professional.id
            dict['name'] = professional.name
            dict['address'] = professional.address
            dict['pincode'] = professional.pincode
            dict['service_type'] = professional.service_type
            dict['experience'] = professional.experience
            dict['document'] = professional.document
            dict['status'] = professional.status
            dict['date_created'] = professional.date_created.strftime('%Y-%m-%d %H:%M:%S')
            all_professionals.append(dict)
        return all_professionals,200
    
    @auth_required('token')
    def put(self):
        data = request.get_json()
        professional_id = data.get('id')
        action = data.get("action")
        professional = Professional.query.filter_by(id=professional_id).first()
        if not professional:
            return "Professional not found",404
        if action == 'approve':
            professional.status = 'approved'
            db.session.commit()
            return "Professional Approved Successfully",201
        elif action == 'reject':
            professional.status = 'rejected'
            db.session.commit()
            return "Professional Rejected Successfully",201
        elif action == 'block':
            professional.status = 'blocked'
            db.session.commit()
            return "Professional Blocked Successfully",201
        elif action == 'unblock':
            professional.status = 'approved'
            db.session.commit()
            return "Professional Unblocked Successfully",201
        return "Invalid action",400
    
class customerAPI(Resource):
    @auth_required('token')
    def get(self):
        customers = Customer.query.all()
        all_customers = []
        for customer in customers:
            dict = {} 
            dict['id'] = customer.id
            dict['name'] = customer.name
            dict['address'] = customer.address
            dict['pincode'] = customer.pincode
            dict['status'] = customer.status
            all_customers.append(dict)
        return all_customers,200
    
    @auth_required('token')
    def put(self):
        data = request.get_json()
        customer_id = data.get('id')
        action = data.get("action")
        customer = Customer.query.filter_by(id=customer_id).first()
        if not customer:
            return "Customer not found",404
        if action == 'block':
            customer.status = 'blocked'
            db.session.commit()
            return "Customer blocked Successfully",201
        elif action == 'unblock':
            customer.status = 'unblocked'
            db.session.commit()
            return "Professional unblocked Successfully",201
        return "Invalid action",400
    
class serviceRequestAPI(Resource):
    @auth_required('token')
    def get(self):
        service_requests = ServiceRequest.query.all()
        all_service_requests = []
        for service_request in service_requests:
            dict = {}
            dict['id'] = service_request.id
            professional = Professional.query.filter_by(id=service_request.professional_id).first()
            customer = Customer.query.filter_by(id=service_request.customer_id).first()
            service = Services.query.filter_by(id=service_request.service_id).first()
            dict['service_name'] = service.name
            dict['customer_name'] = customer.name
            dict['professional_name'] = professional.name
            dict['date_of_request'] = service_request.date_of_request.strftime('%Y-%m-%d %H:%M:%S')
            dict['date_of_completion'] = service_request.date_of_completion
            dict['service_status'] = service_request.service_status
            dict['remarks'] = service_request.remarks
            dict['rating'] = service_request.rating
            all_service_requests.append(dict)
        return all_service_requests,200


class loadChartServiceRequests(Resource):
    @auth_required('token')
    def get(self):     
        user = flask_login.current_user
        customer = Customer.query.filter_by(user_id=user.id).first()
        service_requests = ServiceRequest.query.filter_by(customer_id=Customer.id).all()

        service_request_dict = {}
        service_request_dict['Assigned'] = 0
        service_request_dict['Requested'] = 0
        service_request_dict['Closed'] = 0

        for service_request in service_requests:
            if service_request.service_status == 'assigned':
                service_request_dict['Assigned'] += 1
            elif service_request.service_status == 'requested':
                service_request_dict['Requested'] += 1
            elif service_request.service_status == 'closed':
                service_request_dict['Closed'] += 1

        service_type = list(service_request_dict.keys())
        count = list(service_request_dict.values())

       
        fig, ax = plt.subplots(figsize=(18, 5))
        fig.patch.set_facecolor('#ff000000')  
        bars = ax.bar(service_type, count, color='blue', width=0.4)

         
        for bar in bars:
            bar.set_facecolor('#000')  

        
        ax.set_facecolor('#ff000000')  

        for bar, value in zip(bars, count):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, str(value), ha='center')
            

        ax.set_xlabel("Service Type")  
        ax.set_ylabel("Count")  
        ax.set_title("Service Requests", color='white')  

       
        ax.tick_params(axis='x') 
        ax.tick_params(axis='y')  

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        
        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response

class loadChartAllServiceRequests(Resource):
    @auth_required('token')
    def get(self):     

        service_requests = ServiceRequest.query.all()

        service_request_dict = {}
        service_request_dict['Assigned'] = 0
        service_request_dict['Requested'] = 0
        service_request_dict['Closed'] = 0

        for service_request in service_requests:
            if service_request.service_status == 'assigned':
                service_request_dict['Assigned'] += 1
            elif service_request.service_status == 'requested':
                service_request_dict['Requested'] += 1
            elif service_request.service_status == 'closed':
                service_request_dict['Closed'] += 1

        service_type = list(service_request_dict.keys())
        count = list(service_request_dict.values())

       
        fig, ax = plt.subplots(figsize=(18, 5))
        fig.patch.set_facecolor('#ff000000')  
        bars = ax.bar(service_type, count, color='blue', width=0.4)

         
        for bar in bars:
            bar.set_facecolor('#000')  

        
        ax.set_facecolor('#ff000000')  

        for bar, value in zip(bars, count):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, str(value), ha='center')
            

        ax.set_xlabel("Service Type")  
        ax.set_ylabel("Count")  
        ax.set_title("Service Requests", color='white')  

       
        ax.tick_params(axis='x') 
        ax.tick_params(axis='y')  


        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        
        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    

class loadChartServiceRequestsProfessional(Resource):
    @auth_required('token')
    def get(self):     
        user = flask_login.current_user
        professional = Professional.query.filter_by(user_id=user.id).first()
        service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
        service_request_dict = {}
        service_request_dict['Rejected'] = 0
        service_request_dict['Received'] = 0
        service_request_dict['Closed'] = 0

        for service_request in service_requests:
            if service_request.service_status == 'rejected':
                service_request_dict['Rejected'] += 1
            elif service_request.service_status == 'requested':
                service_request_dict['Received'] += 1
            elif service_request.service_status == 'closed':
                service_request_dict['Closed'] += 1

        service_type = list(service_request_dict.keys())
        count = list(service_request_dict.values())

       
        fig, ax = plt.subplots(figsize=(18, 5))
        fig.patch.set_facecolor('#ff000000')  
        bars = ax.bar(service_type, count, color='blue', width=0.4)

         
        for bar in bars:
            bar.set_facecolor('#000')  

        
        ax.set_facecolor('#ff000000')  

        for bar, value in zip(bars, count):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, str(value), ha='center')
            

        ax.set_xlabel("Service Type")  
        ax.set_ylabel("Count")  
        ax.set_title("Service Requests", color='white')  

       
        ax.tick_params(axis='x') 
        ax.tick_params(axis='y')  

        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        
        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    
class loadChartReviewRatingProfessional(Resource):
    @auth_required('token')
    def get(self):     
        user = flask_login.current_user
        professional = Professional.query.filter_by(user_id=user.id).first()
        service_requests = ServiceRequest.query.filter_by(professional_id=professional.id, service_status='closed').all()
        ratings = [service_request.rating for service_request in service_requests if service_request.rating is not None]
        
        if not ratings:
            return "No ratings available to generate pie chart", 404

        rating_counts = {rating: ratings.count(rating) for rating in set(ratings)}

        labels = list(rating_counts.keys())
        sizes = list(rating_counts.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') 

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    
class loadChartAllReviewRating(Resource):
    @auth_required('token')
    def get(self):     
        service_requests = ServiceRequest.query.filter_by( service_status='closed').all()
        ratings = [service_request.rating for service_request in service_requests if service_request.rating is not None]
        
        if not ratings:
            return "No ratings available to generate pie chart", 404

        rating_counts = {rating: ratings.count(rating) for rating in set(ratings)}

        labels = list(rating_counts.keys())
        sizes = list(rating_counts.values())

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)

        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response


class userVisited(Resource):
    @auth_required("token")
    def post(self):
        user = flask_login.current_user
        
        professional = Professional.query.filter_by(user_id=user.id).first()
        alreadyVisited = userVisit.query.filter_by(professional_id=professional.id).first()
        if alreadyVisited:
            alreadyVisited.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        else:
            visited = userVisit(professional_id=professional.id)
            db.session.add(visited)
        db.session.commit()
        return "",200



class exportServiceRequestCSV(Resource):    
    @auth_required("token")
    def post(self):
        data = request.get_json()
        professional_id = data.get('professional_id')
        professional = Professional.query.filter_by(id=professional_id).first()
        if not professional:
            return "Professional not found",404
        admin = flask_login.current_user
        tasks.export_professional.delay(professional_id,admin.email)
        return jsonify({'message': 'Exporting in progress. You will receive mail once done.'})
