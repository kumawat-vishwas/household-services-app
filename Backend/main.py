import os
from flask import Flask
from flask_restful import Resource,Api
from application import config
from application.config import LocalDevelopmentConfig, TestingConfig
from application.database import db
from application import workers
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role
from flask_login import LoginManager
from flask_cors import CORS 


app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "testing":
      print("Starting Testing")
      app.config.from_object(TestingConfig)
    else:
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()   
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = workers.ContextTask
    app.app_context().push()
    from application.cache import cache
    cache.init_app(app)
    app.app_context().push()
    CORS(app)
    print("Create app complete")
    return app, api, celery, cache

app, api, celery, cache = create_app()


# Import all the controllers so they are loaded
from application.controllers import *

from application.api import userTypeAPI
api.add_resource(userTypeAPI, '/api/get_account_type/<string:email>')

from application.api import checkUserPermission
api.add_resource(checkUserPermission, '/api/checkUserPermission')

from application.api import registerCustomerDetails
api.add_resource(registerCustomerDetails, '/api/registerCustomerDetails')

from application.api import registerProfessionalDetails
api.add_resource(registerProfessionalDetails, '/api/registerProfessionalDetails')

from application.api import checkUserBlockedStatus
api.add_resource(checkUserBlockedStatus, '/api/checkUserBlockedStatus')

from application.api import addUserRole
api.add_resource(addUserRole, '/api/addUserRole')

from application.api import clearCache
api.add_resource(clearCache, '/api/clearCache')

from application.api import updateUserData
api.add_resource(updateUserData, '/api/updateUserData')

from application.api import getAccpetedRejected
api.add_resource(getAccpetedRejected, '/api/getAccpetedRejected')

from application.api import updateServiceHistoryCustomer
api.add_resource(updateServiceHistoryCustomer, '/api/updateServiceHistoryCustomer')

from application.api import getAllServiceTypesName
api.add_resource(getAllServiceTypesName, '/api/getAllServiceTypesName')

from application.api import deleteServiceHistoryCustomer
api.add_resource(deleteServiceHistoryCustomer, '/api/deleteServiceHistoryCustomer/<string:service_request_id>')

from application.api import getServiceDetails
api.add_resource(getServiceDetails, '/api/getServiceDetails/<string:name>')

from application.api import bookProfessional
api.add_resource(bookProfessional, '/api/bookProfessional')

from application.api import closeServiceBooking
api.add_resource(closeServiceBooking, '/api/closeServiceBooking')

from application.api import allServicesbyUser
api.add_resource(allServicesbyUser, '/api/allServicesbyUser')

from application.api import userProfile
api.add_resource(userProfile, '/api/userProfile')

from application.api import professionalProfile
api.add_resource(professionalProfile, '/api/professionalProfile')

from application.api import getAllTodayServices
api.add_resource(getAllTodayServices, '/api/getAllTodayServices')

from application.api import getAllClosedServices
api.add_resource(getAllClosedServices, '/api/getAllClosedServices')

from application.api import rejectServiceRequest
api.add_resource(rejectServiceRequest, '/api/rejectServiceRequest')

from application.api import acceptServiceRequest
api.add_resource(acceptServiceRequest, '/api/acceptServiceRequest')

from application.api import loadChartServiceRequests
api.add_resource(loadChartServiceRequests, '/api/loadChartServiceRequests')

from application.api import loadChartServiceRequestsProfessional
api.add_resource(loadChartServiceRequestsProfessional, '/api/loadChartServiceRequestsProfessional')

from application.api import loadChartReviewRatingProfessional
api.add_resource(loadChartReviewRatingProfessional, '/api/loadChartReviewRatingProfessional')

from application.api import loadChartAllServiceRequests
api.add_resource(loadChartAllServiceRequests, '/api/loadChartAllServiceRequests')

from application.api import loadChartAllReviewRating
api.add_resource(loadChartAllReviewRating, '/api/loadChartAllReviewRating')

from application.api import serviceRequestAPI
api.add_resource(serviceRequestAPI, '/api/getAllServiceRequests')

from application.api import customerAPI
api.add_resource(customerAPI, '/api/getAllCustomers','/api/updateCustomer')

from application.api import professionalAPI
api.add_resource(professionalAPI, '/api/getAllProfessionals','/api/addProfessional','/api/updateProfessional','/api/deleteProfessional/<string:professional_id>')

from application.api import ServicesAPI
api.add_resource(ServicesAPI, '/api/getAllServices','/api/addService','/api/updateService','/api/deleteService/<string:service_id>')

from application.api import userVisited
api.add_resource(userVisited, '/api/userVisited')

from application.api import exportServiceRequestCSV
api.add_resource(exportServiceRequestCSV, '/api/exportCSV')

from application.api import getServicesAvailable
api.add_resource(getServicesAvailable, '/api/getServicesAvailable')



if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)

