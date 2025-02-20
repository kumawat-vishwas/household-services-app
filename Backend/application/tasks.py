from application.workers import celery
from celery import shared_task
from datetime import datetime,timedelta
from flask import current_app as app
from application.models import userVisit, User, Professional,Customer, Role, ServiceRequest, Services
import pytz
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from celery.schedules import crontab

# Define the IST timezone using pytz
ist_timezone = pytz.timezone('Asia/Kolkata')

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=1, day_of_week='*'),
        send_daily_reminders.s(),
    )
    #Executes on 1st day of every month
    sender.add_periodic_task(
        crontab(minute=0, hour=0, day_of_month=1),
        monthly_report.s(),
    )

# SMTP Configuration
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "admin@householdservices.com"
SENDER_PASSWORD = "" 

def send_email(to_address, subject, message, content="text", attachment_file=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "html" if content == "html" else "plain"))

        if attachment_file:
            with open(attachment_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={attachment_file.split('/')[-1]}")
                msg.attach(part)

        with smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT) as s:
            s.ehlo()
            # s.starttls()  # Enable TLS
            s.send_message(msg)

        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email to {to_address}: {e}")

def format_message(template_file, data, email):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, email=email)

def daily_reminder(email):
    message = format_message("templates/notVisited.html", data=email, email=email)
    send_email(
        to_address=email,
        subject="You haven't visited Household Services App Today.",
        message=message,
        content="html",
    )

@celery.task(name='send_daily_reminders')
def send_daily_reminders():
    print("Starting daily reminders...")
    professionals = Professional.query.all()
    user_not_visited = []

    for professional in professionals:
        user_visited = userVisit.query.filter_by(professional_id=professional.id).first()
        user = User.query.filter_by(id=professional.user_id).first()

        if user_visited:
            date_visited = user_visited.timestamp.date()  # Get the date directly
            today_date = datetime.now().date()  # Current date

            if date_visited != today_date:
                user_not_visited.append(user.email)
        else:
            user_not_visited.append(user.email)

    # Send reminders to users who haven't visited
    for email in user_not_visited:
        daily_reminder(email)

    return 'Daily reminders sent'

@celery.task(name='monthly_report')
def monthly_report():
    current_time = datetime.now()
    monthBefore = current_time - timedelta(days=30)
    customer = Customer.query.all()
    for cust in customer:
        service_request = ServiceRequest.query.filter_by(customer_id=cust.id).all()
        user = User.query.filter_by(id=cust.user_id).first()
        assigned = 0
        requested = 0
        closed = 0
        for sr in service_request:
            if sr.service_status == "assigned":
                assigned += 1
            elif sr.service_status == "requested":
                requested += 1
            elif sr.service_status == "closed":
                closed += 1
        data = {"name":cust.name,"assigned":assigned, "requested":requested, "closed":closed}
        message = format_message("templates/monthlyReport.html", data=data, email = user.email)
        send_email(
            to_address=user.email,
            subject="Monthly Report",
            message=message,
            content="html",
        )
    return "Monthly report sent"



@celery.task(name='export_professional')
def export_professional(professional_id, admin_email):
    # Get professional details
    professional = Professional.query.filter_by(id=professional_id).first()
    if not professional:
        return 'Professional not found', 404

    service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()
    
    content = [["Service Name", "Service Request ID", "Date of request", "Status", "Date of Completion", "Rating", "Remarks"]]
    for sr in service_requests:
        service = Services.query.filter_by(id=sr.service_id).first()
        service_name = service.name if service else "Unknown Service"
        service_request_id = sr.id
        date_of_request = sr.date_of_request
        status = sr.service_status
        date_of_completion = sr.date_of_completion
        rating = sr.rating
        remarks = sr.remarks
        content.append([service_name, service_request_id, date_of_request, status, date_of_completion, rating, remarks])
        
    # Initialize csv_content
    csv_content = f"Professional Name,Service Type,Experience,Address,Pincode\n"
    csv_content += f"{professional.name},{professional.service_type},{professional.experience},{professional.address},{professional.pincode}\n"

    csv_content += "\nService Requests:\n"
    csv_content += ",".join(content[0]) + "\n"  
    # Write the service request data
    for line in content[1:]:
        csv_content += ",".join(map(str, line)) + "\n"

    csv_file_path = f"professional_id_{professional_id}.csv"
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_file.write(csv_content)

    # Send email notification to user
    subject = f"{professional.name} CSV Data"
    attached_file = csv_file_path
    message = f"CSV Attachment - {professional.name}"
    send_email(
        to_address=admin_email,
        subject=subject,
        message=message,
        content="html",
        attachment_file=attached_file
    )

    return 'CSV Exported Successfully'
