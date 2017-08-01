from flask import Flask, jsonify, session, redirect, url_for, escape,make_response, request
from flask import render_template
import mysql.connector
import click

app = Flask(__name__)

@app.route('/')
def index():
  if 'username' in session:
    username = session['username']
    resp = make_response(jsonify(
      user_name=username
    ))
    return resp
  return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    session['username'] = request.form['username']
    return redirect(url_for('index'))
  return '''
    <form method="post">
      <p><input type=text name=username>
      <p><input type=submit value=Login>
    </form>
  '''

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  return redirect(url_for('index'))

@app.route('/json')
def return_json():
  resp = make_response(jsonify(
    id=12,
    user_name="username",
    email='email'
  ))
  app.logger.debug('A value for debugging')
  app.logger.warning('A warning occurred (%d apples)', 42)
  app.logger.error('An error occurred')
  resp.set_cookie('id', '123')
  resp.set_cookie('value', 'value', httponly=False)
  return resp

@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404

# customizer flash command(execute: flask initdb)
@app.cli.command()
def initdb():
  """Initialize the database."""
  click.echo('Init the db')

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/currency')
def return_currency():
  conn = mysql.connector.connect(user='root', password='root', database='currency', use_unicode=True)
  cursor = conn.cursor()
  cursor.execute('select * from rates where currency_code = %s', (22,))
  values = cursor.fetchall()
  myList = []
  for v in values:
    row = {'rate': v[3], 'date': v[1].strftime("%Y-%m-%d")}
    myList.append(row)
  resp = make_response(jsonify(
    currency=myList
  ))
  cursor.close()
  conn.close()
  return resp

