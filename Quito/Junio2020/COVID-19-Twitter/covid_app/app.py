import os
from flask import Flask, request, render_template, make_response, flash, redirect
from flask_pymongo import PyMongo
from datetime import date
from forms import LoginForm


from mystats import MyStats as m


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
year = date.today().year


@app.route('/credits', methods=['GET'])
def credits():
    return render_template('credits.html', title='Créditos', year=year)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Login requested for user {}'.format(form.username.data))
            name = form.username.data
            data = m.get_data()
            return render_template('chart.html', title='Stats', name=name, data=data, year=year)
    elif request.method == 'GET':
        return render_template('index.html', title='Inicio de Sesión', form=form, year=year)


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html', title='404'), 404)
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
