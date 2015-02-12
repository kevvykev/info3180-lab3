"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import smtplib
from app import app
from flask import render_template, request, redirect, url_for


###
# Routing for your application.
###

def sendmail(fromname,fromaddr,subject,msg):
  # Credentials (if needed)

  username = 'kevyg123@gmail.com'

  password = 'hbodojywustkxeou'

  # The actual mail send

  server = smtplib.SMTP('smtp.gmail.com:587')

  server.starttls()
  server.login(username,password)
  toaddrs = 'kevyg123@gmail.com'
  message = """From: {} <{}>

  To: {} <{}>

  Subject: {}

  {}

  """
  toname = 'David Bain'

  messagetosend = message.format(
   fromname,
   fromaddr,
   toname,
   toaddrs,
   subject,
   msg)
  server.sendmail(fromaddr, toaddrs, messagetosend)

  server.quit()
  return True

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route('/contact/', methods=["POST", "GET"])
def contact():
  """Render webpage contact"""
  if request.method == "POST":
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    
    if sendmail(fromname=name,
                fromaddr=email,
                subject=subject,
                msg=message):
      return render_template("contact.html",
                             status="Mail sent"
                            )
  return render_template('contact.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")