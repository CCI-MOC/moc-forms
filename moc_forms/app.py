import flask
import flask_bootstrap
import flask_wtf
import wtforms
from wtforms import validators

from moc_forms import adjutant
from moc_forms import config

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'
flask_bootstrap.Bootstrap(app)

CONF = config.CONF


class SignUpForm(flask_wtf.FlaskForm):
    name = wtforms.StringField('Name')
    email = wtforms.StringField('Email')
    organization = wtforms.StringField('Organization',
                                       validators=[validators.DataRequired()])
    organization_role = wtforms.SelectMultipleField(
        'Role',
        choices=[('student', 'Student'),
                 ('staff', 'Staff'),
                 ('faculty', 'Faculty'),
                 ('other', 'Other')],
        validators=[validators.DataRequired()]
    )
    organization_role_other = wtforms.StringField('Role (if other)')
    project_name = wtforms.StringField('Project Name',
                                       validators=[validators.DataRequired()])
    project_description = wtforms.TextAreaField('Project Description',
                                                validators=[validators.DataRequired()])
    project_services = wtforms.SelectMultipleField(
        'Services',
        choices=[('openstack-kaizen', 'OpenStack Kaizen')],
        validators=[validators.DataRequired()]
    )
    project_moc_sponsor = wtforms.StringField('MOC Sponsor for Project',
                                              validators=[validators.DataRequired()])
    submit = wtforms.SubmitField()


@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        r = adjutant.SignUpRequest(**form.data)
        return flask.render_template('success.html')

    data = {
        'name': 'Test User',
        'email': 'testemail@bu.edu',
        'organization': 'Boston University'
    }
    for key, value in data.items():
        if key in form:
            form[key].render_kw = {'value': value, 'readonly': True}

    return flask.render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(port=5001)
