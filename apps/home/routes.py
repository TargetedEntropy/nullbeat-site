# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests

@blueprint.route('/index.html')
@login_required
def index():
    try:
        stats = requests.get("http://10.0.0.39:8000/stats")
    except Exception as error:
        raise Exception(f"Unable to get access API Data, error: {error}")
        
    return render_template('home/index.html', segment='index', stats_data=stats.json())


@blueprint.route('/storage.html')
@login_required
def route_storage():

    try:
        req = requests.get("http://10.0.0.39:8000/item")
    except Exception as error:
        raise Exception(f"Unable to get access API Data, error: {error}")
        

    data = req.json()
    import json
    all_data = []
    for d in data:

        item_data = {}
        item_name = d['item_name']
        contents = json.loads(d['item_contents'])

        item_contents = []
        for content in contents:
            item_id = content['id']
            item_id = item_id.replace("minecraft:", "")
            item_id = item_id.replace("_", "-")
            
            item_contents.append(item_id)

        item_data['item_name'] = item_name
        item_data['item_contents'] = item_contents
        all_data.append(item_data)
        
        


    try:

        # Detect the current page
        segment = get_segment(request)
        # print(req.json())
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/storage.html", segment=segment, json_data=all_data)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

# @blueprint.route('/<template>')
# @login_required
# def route_template(template):

#     try:

#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)

#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     except:
#         return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
