from datetime import datetime
from django.db import models
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.core.files import File
import os
from django.conf import settings
import pdfkit
import pytz
# from rlextra.rml2pdf import rml2pdf
# import cStringIO
# from reportlab.pdfgen import canvas

def fetch_resources(uri, rel):
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    return path
 
def generate_pdf(template_name, context_dict={}, css_name=None):
    html = render_to_string(template_name, context_dict)
    # css_path = 'static/style.css'
    # if css_name:
    #     css_path = css_name
    # css = os.path.join(os.path.dirname(__file__), css_path)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None,
        "quiet": "",
        'margin-top': '0.05in',
        'margin-right': '0.05in',
        'margin-bottom': '0.05in',
        'margin-left': '0.05in',
        'encoding': "UTF-8",
        'no-outline': None,
        'page-size':'A4'
        # 'javascript-delay':'2000'
    }
    pdf = pdfkit.from_string(html, configuration=config,  options=options)
    output = BytesIO()
    output.write(pdf)
    output.seek(0)
    return HttpResponse(output.getvalue(), content_type='application/pdf')

def get_key_from_value(dict:dict, value):
    try:
        return next(x for x,y in dict.items() if y == value)
    except:
        return None
    
def localize_datetime(dt:datetime):
    tz = pytz.timezone('Europe/Rome')
    return tz.localize(dt)