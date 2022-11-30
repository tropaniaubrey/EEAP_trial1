from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import make_password
# from .forms import sign_up
# from django.contrib.auth.forms import UserCreationForm

from django.core.mail import send_mail

import os
from os import *

from datetime import date

from .models import *
from qrcode import *

import io
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle, colors

# Create your views here.


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        birthday = request.POST.get('birthday')
        print(password)
        user = authenticate(request, username=username,
                            password=password, birthday=birthday)
        if user is not None and user.usertype == 'STUDENT':
            login(request, user)
            return redirect('student_dashboard')
        elif user is not None and user.usertype == 'ADMIN':
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'html/homepage.html')


@login_required(login_url='index')
def student_dashboard(request):
    username = request.user.username
    if request.user.is_authenticated and request.user.usertype == 'STUDENT':
        if request.method == "POST":
            date = request.POST.get('DATE')

            students = log_record.objects.filter(idnumber=username)
            user = accounts.objects.filter(idnumber=username)

            students = log_record.objects.filter(idnumber=username, date=date)
            user = accounts.objects.filter(idnumber=username)
            context = {'students': students, 'user': user}
            return render(request, 'html/student_dashboard.html', context)

        students = log_record.objects.filter(idnumber=username)
        user = accounts.objects.filter(idnumber=username)
        context = {'students': students, 'user': user}
        return render(request, 'html/student_dashboard.html', context)
    return redirect('index')


@login_required(login_url='index')
def vehicle_registration(request):
    username = request.user.username
    if request.user.is_authenticated and request.user.usertype == 'STUDENT':
        if request.method == "POST":
            vehicles_info = registered_vehicles.objects.filter(
                idnumber=username)

            if len(vehicles_info) < 2:
                plate_number = request.POST.get('plnum')
                vehicle_model = request.POST.get('vehicle')
                imageF = request.FILES['imageF']
                imageL = request.FILES['imageL']
                imageR = request.FILES['imageR']
                imageB = request.FILES['imageB']
                ORCR = request.FILES['ORCR']
                username = request.user.username

                vehicle_id = username + "-" + plate_number

                vehicle = registered_vehicles.objects.create(vehicleid=vehicle_id, idnumber=username,
                                                             platenumber=plate_number, vehiclemodel=vehicle_model, imageF=imageF, imageL=imageL, imageR=imageR,
                                                             imageB=imageB, ORCR=ORCR, status='PENDING')
                vehicle.save()
        user = accounts.objects.filter(idnumber=username)
        context = {'user': user}
        return render(request, 'html/vehicle_registration.html', context)
    return redirect('index')


@login_required(login_url='index')
def registered_vehicle(request):
    username = request.user.username
    if request.user.is_authenticated and request.user.usertype == 'STUDENT':
        username = request.user.username
        if request.method == "POST":
            ids = request.POST.get('id')
            vehicle_status_delete = registered_vehicles.objects.get(
                vehicleid=ids)
            vehicle_status_delete.delete()

        user = accounts.objects.filter(idnumber=username)
        vehicles_info = registered_vehicles.objects.filter(
            idnumber=username, status="ACCEPTED")

        context = {'vehicles_info': vehicles_info, 'user': user}

        return render(request, 'html/registered_vehicle.html', context)
    return redirect('index')


@login_required(login_url='index')
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.usertype == 'ADMIN':
        username = request.user.username
        if request.method == "POST":
            id = request.POST.get('ID')
            course = request.POST.get('COURSE')
            date = request.POST.get('DATE')
            action = request.POST.get('ACTION')

            if action == "ID":
                log_record.objects.all()
                accounts.objects.all()
                registered_vehicles.objects.all()

                record = log_record.objects.filter(idnumber=id)
                student = accounts.objects.filter(idnumber=id)
                vehicle = registered_vehicles.objects.filter(idnumber=id)
                context = {'record': record,
                           'student': student, 'vehicle': vehicle}
                return render(request, 'html/admin_dashboard.html', context)
            elif action == 'COURSE':
                record = log_record.objects.all()
                student = accounts.objects.all()
                vehicle = registered_vehicles.objects.all()

                record = log_record.objects.all()
                student = accounts.objects.filter(course=course)
                vehicle = registered_vehicles.objects.all()
                context = {'record': record,
                           'student': student, 'vehicle': vehicle}
                return render(request, 'html/admin_dashboard.html', context)
            elif action == 'DATE':
                record = log_record.objects.all()
                student = accounts.objects.all()
                vehicle = registered_vehicles.objects.all()

                record = log_record.objects.filter(date=date)
                student = accounts.objects.all()
                vehicle = registered_vehicles.objects.all()
                context = {'record': record,
                           'student': student, 'vehicle': vehicle}
                return render(request, 'html/admin_dashboard.html', context)
            # elif action == 'TRANSCRIBE':
            #     record = log_record.objects.all()
            #     student = accounts.objects.all()
            #     vehicle = registered_vehicles.objects.all()

            #     my_path = 'C:\Users\Cristian Ausena\Downloads\Outputthesis Update\New folder\Outputthesis\\logbook.pdf '
            #     my_data = [['Date', 'Time In', 'Time Out', 'First Name', 'Last Name',
            #                 'GSFE', 'ID Number', 'Course', 'Year', 'Contact Number', 'Vehicle ID']]
            #     # for i in record:
            #     #     for x in student:
            #     #         for y in vehicle:
            #     #             z = (i.first_name + ' ' + i.last_name, i.checkin_date, i.checkout_date, i.contact_num,
            #     #                 i.email, i.room_name, i.guest, i.num_of_days, i.activity, i.code, i.price)
            #     #             my_data.append(i)
            #     #             print(i)
            #     #         print(my_data)
            #     #         my_doc = SimpleDocTemplate(my_path, pagesize=landscape(A4))
            #     #         t = Table(my_data, rowHeights=20, repeatRows=1)
            #     #         t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            #     #                             ('FONTSIZE', (0, 0), (-1, -1), 10)]))
            #     #         elements = []
            #     #         elements.append(t)
            #     #         my_doc.build(elements)
            #     return render(request, 'html/admin_dashboard.html', context)

        record = log_record.objects.all()
        student = accounts.objects.all()
        vehicle = registered_vehicles.objects.all()
        user = accounts.objects.filter(idnumber=username)
        context = {'record': record, 'student': student,
                   'vehicle': vehicle, 'user': user}
        return render(request, 'html/admin_dashboard.html', context)
    return redirect('index')


@login_required(login_url='index')
def pending_vehicle(request):
    if request.user.is_authenticated and request.user.usertype == 'ADMIN':
        username = request.user.username
        if request.method == "POST":
            actions = request.POST.get('actions')
            ids = request.POST.get('id')
            print(actions, ids)

            if actions == "ACCEPT":
                vehicle_status_update = registered_vehicles.objects.get(
                    vehicleid=ids)
                user2 = accounts.objects.get(
                    idnumber=vehicle_status_update.idnumber)
                print(user2.email)
                vehicle_status_update.status = "ACCEPTED"

                send_mail(
                    'Confirmation',
                    'Good Day! Your vehicle application (' + str(
                        vehicle_status_update.vehicleid) + ') has been approved. Visit your logbook portal for QR Code',
                    'tropaniaubrey@gmail.com',
                    [user2.email],)

                admin = accounts.objects.get(idnumber=username)

                vehicle_status_update.approved_by = admin.first_name + admin.last_name
                vehicle_status_update.date_approved = str(date.today())

                img = make(vehicle_status_update.vehicleid + "-V")
                img_name = vehicle_status_update.vehicleid + '.png'
                img.save(settings.MEDIA_ROOT + '/' + img_name)
                vehicle_status_update.qrcode = img_name
                vehicle_status_update.save()

            else:
                vehicle_status_delete = registered_vehicles.objects.get(
                    vehicleid=ids)
                user2 = accounts.objects.get(
                    idnumber=vehicle_status_delete.idnumber)

                send_mail(
                    'Confirmation',
                    'Good Day! Your vehicle application (' + str(
                        vehicle_status_delete.vehicleid) + ') has been declined.',
                    'tropaniaubrey@gmail.com',
                    [user2.email],)

                vehicle_status_delete.delete()

        vehicle_image = registered_vehicles.objects.filter(status="PENDING")
        user = accounts.objects.filter(idnumber=username)
        user2 = accounts.objects.all()
        context = {'vehicle_image': vehicle_image,
                   'user': user, 'user2': user2}
        return render(request, 'html/pending_vehicle.html', context)
    return redirect('index')


@login_required(login_url='index')
def student_registration(request):
    if request.user.is_authenticated and request.user.usertype == 'ADMIN':
        username = request.user.username
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            birthday = request.POST.get('birthday')
            idnumber = request.POST.get('idnumber')
            contactnumber = request.POST.get('contactnumber')
            course = request.POST.get('course')
            year = request.POST.get('year')
            usertype = request.POST.get('usertype')
            student_pic = request.FILES['student_pic']

            pass1 = idnumber + "-" + last_name.upper()
            pass2 = idnumber + "-" + last_name.upper() + "-S"

            password = make_password(pass1)

            new_bd = birthday[5:7] + "/" + birthday[8:] + "/" + birthday[0:4]

            img = make(pass2)
            img_name = "ID-" + pass1 + '.png'
            img.save(settings.MEDIA_ROOT + '/' + img_name)

            account = accounts.objects.create(first_name=first_name, last_name=last_name,
                                              email=email, birthday=new_bd, idnumber=idnumber, contactnumber=contactnumber, course=course,
                                              year=year, username=idnumber, password=password, usertype=usertype, student_pic=student_pic, student_qr=img_name)
            account.save()

            send_mail(
                'Confirmation',
                'Good Day! You are now registered on TUPC Logbook. To access your logbook, visit the website (link) and use your student ID number as Username and Pasword in this format (TUPC-00-0000-LASTNAME)',
                'tropaniaubrey@gmail.com',
                [email],)

        user = accounts.objects.filter(idnumber=username)
        context = {'user': user}
        return render(request, 'html/student_registration.html', context)
    return redirect('index')

# @login_required(login_url='index')
# def student_registration(request):
#     if request.user.is_authenticated and request.user.usertype == 'ADMIN':
#         form = sign_up
#         username = request.user.username
#         if request.method == "POST":
#             form = sign_up(request.POST)
#             if form.is_valid():
#                 form.save()
#         user = accounts.objects.filter(idnumber=username)
#         context = {'user': user, 'form' : form}
#         return render(request, 'html/student_registration.html',context)
#     return redirect ('index')


def logoutuser(request):
    logout(request)
    return redirect('index')
