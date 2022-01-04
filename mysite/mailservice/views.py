from django.shortcuts import render, HttpResponse
from .models import MailService
import requests
import os
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
# Create your views here.

def index(request):
    if request.method == 'POST':
        #Taking inputs from POST Method
        name = request.POST.get('name')
        mail_id = request.POST.get('email')
        city = request.POST.get('city')
        #Saving data into Sqlite Database
        make_entry = MailService(name=name,email=mail_id,city=city)
        make_entry.save()
        #Fetching data from OpenWeatherMap API
        baseurl = 'http://api.openweathermap.org/data/2.5/weather?appid='+str(os.getenv('API_KEY'))+'&q='+city
        weatherData = requests.get(baseurl)
        finalData = weatherData.json()
        print(finalData)
        tempData = finalData['main']
        #Converting Kalvin into Celsius
        current_temp = tempData['temp'] - 273.15
        #Deciding what is the the temperature i.e Cold,Humid,Hot
        img_name=""
        if current_temp <= 18.00: 
            img_name='cold.jpg'
        elif current_temp > 19.00 and current_temp <= 28.00:
            img_name='sunny.jfif'
        else:
            img_name='hot.jpg'
        print(current_temp)
        #Mail Service
        subject = "Hii "+name+" interested in our services"
        body_html = '''
            <html>
                <body>
                    <h4>{TEMP}</h4>
                    <img src="{URL}" />
                </body>
            </html>
        '''
        current_temp = "{:.2f}".format(current_temp)
        body_html = body_html.format(URL='cid:'+img_name,TEMP='Temperature : '+current_temp+' Celsius')
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
        subject,
        body_html,
        from_email=from_email,
        to=[mail_id]
        )
        msg.mixed_subtype = 'related'   
        msg.attach_alternative(body_html, "text/html")
        img_dir = 'static'
        image = img_name
        file_path = os.path.join(img_dir, image)
        
        with open(file_path,'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
        msg.attach(img)
        msg.send()
        return render(request,'index.html')
    else:
        return render(request,'index.html')

