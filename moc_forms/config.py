# Copyright (c) 2018 Kristi Nikolla
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from os import path

from oslo_config import cfg

CONF = cfg.CONF

default_opts = [
    cfg.StrOpt('adjutant_url',
               default='http://localhost:5000/v1',
               help='Registration endpoint. (v1)'),

    cfg.StrOpt('keystone_url',
               default='http://devstack/identity/v3',
               help='Identity endpoint. (v3)'),

]
CONF.register_opts(default_opts)

oidc_group = cfg.OptGroup(name='oidc',
                          title='OpenID Connect Auth Group')
oidc_opts = [
    cfg.StrOpt('authorization_endpoint',
               default='https://sso.massopen.cloud/auth/realms/moc/protocol/openid-connect/auth',
               help='OAuth 2.0 Authorize Endpoint.'),

    cfg.StrOpt('token_endpoint',
               default='https://sso.massopen.cloud/auth/realms/moc/protocol/openid-connect/token',
               help='OAuth 2.0 Authorize Endpoint.'),

    cfg.StrOpt('logout_endpoint',
               default='https://sso.massopen.cloud/auth/realms/moc/protocol/openid-connect/logout',
               help='OAuth 2.0 End Session Endpoint'),

    cfg.StrOpt('client_id',
               default='',
               help='OAuth 2.0 Client ID.'),

    cfg.StrOpt('client_secret',
               default='',
               help='OAuth 2.0 Client Secret.'),
]
CONF.register_group(oidc_group)
CONF.register_opts(oidc_opts, oidc_group)


def load_config():
    conf_files = [f for f in ['moc-forms.conf',
                              'etc/moc-forms.conf',
                              '/etc/moc-forms.conf'] if path.isfile(f)]
    if conf_files is not []:
        CONF(default_config_files=conf_files)


def list_opts():
    return [(None, default_opts),]
