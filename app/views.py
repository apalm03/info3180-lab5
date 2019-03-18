"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import UserProfile
from app.forms import UserProfileForm
from werkzeug.utils import secure_filename
import time 
import datetime
import os



###
# Routing for your application.
###

def format_date_joined():
    """returns the date in the format Month, Year (for example Feb, 2018)"""
    return datetime.date.today().strftime("%b, %d,%Y")


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name = "Aaron Myrie")

    
@app.route('/profile', methods=["GET", "POST"])
def profile():
    userProfileForm = UserProfileForm()
    
    if request.method == "POST" and userProfileForm.validate_on_submit():
        firstname = userProfileForm.fname.data
        lastname = userProfileForm.lname.data
        gender = userProfileForm.gender.data
        email = userProfileForm.email.data
        location = userProfileForm.location.data
        bio = userProfileForm.bio.data
        made_on = format_date_joined()
        photo = userProfileForm.photo.data
        image = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], image))
        user = UserProfile(first_name = firstname, last_name = lastname, gender = gender, email = email, location = location, bio = bio, image = image, created_on = made_on)
        db.session.add(user)
        db.session.commit()
                
        flash("Profile was successfully added", "success")
        return redirect(url_for("profiles"))
    flash_errors(userProfileForm)
    return render_template("profile.html", userProfileForm = userProfileForm)
    
@app.route('/profiles')
def profiles():
    pic_names= get_uploaded_photos()
    users = db.session.query(UserProfile).all()
    
    if request.method == 'GET':
        return render_template('profiles.html', users = users, pic_names= pic_names)
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        users_lst = []
        for user in users:
            users_lst += [{"userid":user.get_id, "firstname": user.first_name,"lastname": user.last_name, "gender": user.gender, "location":user.location}]
        json_user = {"users":users_lst}
        return jsonify(json_user)
    else:
        flash('No user was found', 'danger')
        return redirect(url_for('home'))
    
 
@app.route('/profile/<userid>')
def userProfile(userid):
    user = UserProfile.query.filter_by(id=userid).first()
    pic_names= get_uploaded_photos()
    
    if request.method=='GET':
        return render_template('user_profile.html', user =user, pic_names=pic_names)
    elif request.method == "POST" and request.headers['Content-Type'] == "application/json":
        json_user = {}
        json_user["userid"] = user.id
        json_user["username"] = user.first_name + user.last_name
        json_user["email"] = user.email
        json_user["location"] = user.location
        json_user["bio"] = user.bio
        json_user["profile_created_on"] = user.created_on
        json_user["image"] = user.id + '.jpg'
        return jsonify(json_user)
    return render_template('user_profile.html', user=user, pic_names=pic_names)
    
 

def get_uploaded_photos():
    
    #Get contents of Current working directory
    rootdir = os.getcwd()
    print (rootdir)
    filenames = []
            
    #Traversing root directory recursively
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
	    for file in files:
	        filenames.append(os.path.join(subdir, file).split('/')[-1])
    return filenames

###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")