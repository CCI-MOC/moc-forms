import logging

import flask
import flask_bootstrap
import flask_oidc
import flask_wtf
import wtforms
from wtforms import validators

from moc_forms import adjutant
from moc_forms import config

app = flask.Flask(__name__)

app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'OIDC_CLIENT_SECRETS': 'secrets/client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OVERWRITE_REDIRECT_URI': 'https://service-onboarding.k-apps.osh.massopen.cloud/oidc_callback'
})

oidc = flask_oidc.OpenIDConnect(app)
flask_bootstrap.Bootstrap(app)

CONF = config.CONF

logging.basicConfig(level=logging.DEBUG)


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
        default=('openstack-kaizen', 'OpenStack Kaizen'),
        render_kw={'readonly': True},
        validators=[validators.DataRequired()]
    )
    project_moc_sponsor = wtforms.StringField('MOC Sponsor for Project',
                                              validators=[validators.DataRequired()])
    submit = wtforms.SubmitField()


@app.route('/signup', methods=('GET', 'POST'))
@oidc.require_login
def signup():
    access_token = oidc.get_access_token()
    if not access_token:
        # Note(knikolla): It somehow seems that we can get through
        # this even when there isn't an access token in the server
        # MemoryCredentials store. Enforce a redirect and never
        # let the user go through without a valid access token.
        return oidc.redirect_to_auth_server(destination='/signup')

    form = SignUpForm()
    if form.validate_on_submit():
        r = adjutant.SignUpRequest(**form.data)
        return flask.render_template('success.html')

    data = {
        'name': "%s %s" % (oidc.user_getfield('given_name'), oidc.user_getfield('family_name')),
        'email': oidc.user_getfield('email'),
        'organization': oidc.user_getfield('organization') if oidc.user_getfield('organization') not in [
            'GitHub', 'Google'] else None
    }
    # TODO(knikolla): Get affilication from id_token

    logging.info(oidc.get_access_token())

    for key, value in data.items():
        if key in form and value:
            form[key].render_kw = {'value': value, 'readonly': True}

    return flask.render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
