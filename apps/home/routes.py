# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.main import Argon

model = Argon()


@blueprint.route('/model-init', methods=["GET", "POST"])
@login_required
def model_init():

    if request.method == "POST":
        id    = request.form["Model"]
        ticker   = request.form["Ticker"]
        optimize = True if request.form.get('Optimize') else False
        
        try:
            model.setModel(100000, id, ticker, optimize)
            print('variables are set')
        except KeyError as error:
            return render_template('home/model-init.html', segment='dashboard', msg=error)
        except ValueError as error:
            return render_template('home/model-init.html', segment='dashboard', msg=error)    

        return redirect('/dashboard', code=302)
    else:
        return render_template('home/model-init.html', segment='dashboard')

@blueprint.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    
    try:
        stats = model.getStats()
    except Exception as error:
        return redirect('/model-init', code=302)
    
    if request.method == "POST":
        if request.form.get('plot-btn'):
            model.plot(stats)
        elif request.form.get('back-btn'):
            return redirect('/model-init', code=302)
        
    return render_template('home/dashboard.html', segment='dashboard', stats=stats, id=model.id, ticker=model.ticker, optimize=model.optimize)

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'model-init'

        return segment

    except:
        return None
