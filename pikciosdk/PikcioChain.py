import base64
import json
import os

import requests
import time
from flask import Flask, jsonify, abort, make_response, redirect, request, \
    url_for
from flask_oauthlib.client import OAuth
from selenium import webdriver

from config import get_config
from log import Logger

access_token = ''


def init_api_client():
    """
    Initialize Flask API Client
    This is necessary for the grant code method
    """

    log = Logger()
    config = get_config()
    app_name = config.get('application', 'name')
    app = Flask('{0}_api_client'.format(app_name), template_folder='templates')

    os.environ['DEBUG'] = 'true'

    try:
        client_id = config.get('api_client', 'client_id')
        client_secret = config.get('api_client', 'client_secret')
        public_ip_server = config.get('server', 'public_ip')
        public_port_server = config.get('server', 'public_port')
        private_ip_server = config.get('server', 'public_ip')
        private_port_server = config.get('server', 'public_port')
        https = config.get('server', 'tls')
        redirect_uri = config.getboolean('server', 'redirect_uri')
    except Exception as e:
        log.error('init_api_client Exception : {0}'.format(e))
        return json.dumps("Invalid config file")

    @app.route('/api/authorized')
    def grant_code():
        try:
            global access_token
            # get access token with the authorization_code method
            # to be able to use the access token easily, we store it in a
            # global variable
            code = request.args.get('code')

            data = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': redirect_uri
            }

            if https:
                p = requests.post(
                    url='https://' + public_ip_server + ':' +
                        public_port_server + '/oauth/token',
                    data=data, verify=False)
            else:
                p = requests.post(
                    url='http://' + public_ip_server + ':' +
                        public_port_server + '/oauth/token',
                    data=data, verify=False)
            access_token = p.json().get('access_token')

            if not access_token:
                # we try with private ip
                if https:
                    p = requests.post(
                        url='https://' + private_ip_server + ':' +
                            private_port_server + '/oauth/token',
                        data=data, verify=False)
                else:
                    p = requests.post(
                        url='http://' + private_ip_server + ':' +
                            private_port_server + '/oauth/token',
                        data=data, verify=False)
                access_token = p.json().get('access_token')
            return access_token
        except Exception as ex:
            log.error('init_api_client Exception : {0}'.format(ex))
        return json.dumps("Invalid config file")

    return app


class ClientAPI:
    """
    Class access for python Client API
    """

    def __init__(self, username=None, password=None):
        config = get_config()
        self.api_public_ip = config.get('server', 'public_ip')
        self.api_public_port = config.get('server', 'public_port')
        self.api_private_ip = config.get('server', 'private_ip')
        self.api_private_port = config.get('server', 'private_port')
        self.client_id = config.get('api_client', 'client_id')
        self.client_secret = config.get('api_client', 'client_secret')
        self.scope = config.get('api_client', 'scope')
        self.method = config.get('api_client', 'auth_type')
        self.https = config.getboolean('server', 'tls')
        self.username = username
        self.password = password

        self.log = Logger(system=self)

        self.app_name = config.get('application', 'name')
        self.app = Flask('{0}_api_client'.format(self.app_name))
        self.oauth = OAuth(self.app)

        os.environ['DEBUG'] = 'true'

        if self.https:
            self.api_base_url = 'https://{0}:{1}/api/'.format(
                self.api_public_ip, self.api_public_port)
            self.access_token_url = 'https://{0}:{1}/oauth/token'.format(
                self.api_public_ip, self.api_public_port)
            self.authorize_url = 'https://{0}:{1}/oauth/authorize'.format(
                self.api_public_ip, self.api_public_port)
        else:
            self.api_base_url = 'http://{0}:{1}/api/'.format(
                self.api_public_ip, self.api_public_port)
            self.access_token_url = 'http://{0}:{1}/oauth/token'.format(
                self.api_public_ip, self.api_public_port)
            self.authorize_url = 'http://{0}:{1}/oauth/authorize'.format(
                self.api_public_ip, self.api_public_port)

        self.remote = self.oauth.remote_app(
            'remote',
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={'scope': self.scope},
            base_url=self.api_base_url,
            request_token_url=None,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url
        )

        self.remote_oauth = ''
        self.access_token = ''
        self.refresh_token = ''
        self.retries = 0
        self.req_initiator_url = ''
        self.web_server = ''

    """
    Everything related to API connection
    """

    def get_oauth_token(self):
        return self.remote_oauth

    def refresh_tok(self):
        token = self.get_oauth_token()
        if token == '' or token[1] == '':
            return self.authorize()

        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': token[1],
            'scope': self.scope,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }
        auth_code = base64.b64encode(
            '{0}:{1}'.format(self.client_id, self.client_secret))
        res = requests.post(self.access_token_url, data=data, headers={
            'Authorization': 'Basic {0}'.format(auth_code)},
                            verify=False)

        if res.status_code == 401:
            self.remote_oauth = ''
            return self.authorize()

        if res.status_code in (200, 201):
            self.remote_oauth = (
                res.json().get('access_token'),
                res.json().get('refresh_token'))
            self.access_token = res.json().get('access_token')
            self.refresh_token = res.json().get('refresh_token')
            return True

        return False

    def require_authorize(self, f):
        """
        Decorator used to validate client authorization; In case the client
        is not authorized, redirect to the Authorize Page, otherwise check
        if the access token expired and request new one using the refresh
        token.

        :return:
        """

        def wrap(*args, **kwargs):
            token = self.get_oauth_token()
            if not token:
                self.req_initiator_url = '/api'
                return redirect('/authorize')

            resp = f(*args, **kwargs)

            if not resp.status or resp.status in (401,):
                token = self.get_oauth_token()
                if token and token[1]:
                    self.refresh_tok()
                else:
                    return redirect('/authorize')

                resp = f(*args, **kwargs)

            return make_response(jsonify(resp.data), resp.status)

        return wrap

    def authorize(self):
        if self.remote_oauth != '':
            return redirect(url_for('api_index'))

        next_url = request.args.get('next') or request.referrer or None

        return self.remote.authorize(
            callback=url_for('authorized', next=next_url, _external=True)
        )

    def authorized(self):
        resp = self.remote.authorized_response()
        # print resp
        if not resp:
            return jsonify(
                error=request.args.get('error'),
                message=request.args.get('error_description') or ''
            )
        elif hasattr(resp, 'data') and resp.data.get('error'):
            return jsonify(
                error=resp.data['error'],
                message=resp.message or ''
            )
        if not resp.get('access_token') or not resp.get('refresh_token'):
            abort(401)

        self.refresh_token = resp['refresh_token']
        self.access_token = resp['access_token']

        if self.req_initiator_url != '':
            req_initiator = self.req_initiator_url
            return redirect(req_initiator)

        return redirect('/api')

    def deauthorize(self):
        if self.remote_oauth != '':
            self.remote_oauth = ''
            self.refresh_token = ''
            self.access_token = ''

        return redirect(url_for('authorize'))

    def api_index(self):
        resp = self.remote.get('home')
        return resp

    def generic_request(self, url, method, params=None):
        global access_token
        try:
            # if we used grant_code method, the access token variable of the
            # class won't be initialised yet
            if self.access_token == '':
                # if the access token hasn't been got yet, we wait 5s and call
                # the function again until the global variable isn't null
                # anymore
                if access_token != '':
                    self.access_token = access_token
                else:
                    self.retries += 1
                    if self.retries == 3:
                        self.retries = 0
                        p = jsonify({
                            'error': 'Too many failed attempts to retrieve '
                                     'access token, please try the password '
                                     'method.'})
                        return p

                    time.sleep(5)
                    return self.generic_request(url, method, params)
            if method.lower() == 'get':
                p = requests.get(
                    url=url + '?access_token=' + self.access_token,
                    verify=False)
            elif method.lower() == 'post':
                p = requests.post(
                    url=url + '?access_token=' + self.access_token,
                    data=params,
                    headers={'Content-Type': 'application/json'}, verify=False)
            elif method.lower() == 'delete':
                p = requests.delete(
                    url=url + '?access_token=' + self.access_token,
                    data=params, verify=False)
            else:
                p = json.dumps('Bad request')
            if p.status_code == 401 and self.retries < 1:
                if self.refresh_tok():
                    self.retries += 1
                    if method.lower() == 'get':
                        p = requests.get(
                            url=url + '?access_token=' + self.access_token,
                            verify=False)
                    elif method.lower() == 'post':
                        p = requests.post(
                            url=url + '?access_token=' + self.access_token,
                            data=params,
                            headers={'Content-Type': 'application/json'},
                            verify=False)
                    elif method.lower() == 'delete':
                        p = requests.delete(
                            url=url + '?access_token=' + self.access_token,
                            data=params, verify=False)
                    else:
                        p = json.dumps('API connexion lost')
            elif p.status_code == 500:
                self.log.error('Server connexion error : {0}'.format(p))
                return json.dumps('Server failure, please report the bug')
            else:
                self.retries = 0
        except Exception as e:
            self.log.error('generic_request Exception : {0}'.format(e))
            return json.dumps('Bad request')

        return p

    def get_access_token(self):
        try:
            if self.method.lower() == 'password_header':
                data = {
                    'grant_type': 'password',
                    'username': self.username,
                    'password': self.password,
                    'scope': self.scope
                }
                auth_code = base64.b64encode(
                    bytes(self.client_id + ':' + self.client_secret))
                try:
                    p = requests.post(url=self.access_token_url, data=data,
                                      headers={
                                          'Authorization': 'Basic {0}'.format(
                                              auth_code)}, verify=False,
                                      timeout=10)
                except (requests.Timeout, requests.ConnectionError):
                    # try with private IP
                    self.log.error('Failed to connect public IP, try to '
                                   'connect private IP')
                    base_url = 'http{0}://{1}:{2}/'.format(
                        's' if self.https else '',
                        self.api_private_ip,
                        self.api_private_port
                    )
                    self.api_base_url = base_url + 'api/'
                    self.access_token_url = base_url + 'oauth/token'
                    self.authorize_url = base_url + 'oauth/authorize'
                    p = requests.post(url=self.access_token_url, data=data,
                                      headers={
                                          'Authorization': 'Basic {0}'.format(
                                              auth_code)}, verify=False,
                                      timeout=10)

                if p and p.status_code == 401:
                    return json.dumps(
                        {'status': False, 'msg': 'API authentication failed'})
                else:
                    self.access_token = p.json().get('access_token')
                    self.refresh_token = p.json().get('refresh_token')
                    self.remote_oauth = (self.access_token, self.refresh_token)
                    return json.dumps(
                        {'status': True, 'msg': 'API access granted'})

            elif self.method.lower() == 'password_data':
                data = {
                    'grant_type': 'password',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'username': self.username,
                    'password': self.password,
                    'scope': self.scope
                }
                try:
                    p = requests.post(url=self.access_token_url, data=data,
                                      verify=False, timeout=10)
                except (requests.Timeout, requests.ConnectionError):
                    # try with private IP
                    self.log.error(
                        'Failed to connect public IP, try to connect private '
                        'IP')
                    base_url = 'http{0}://{1}:{2}/'.format(
                        's' if self.https else '',
                        self.api_private_ip,
                        self.api_private_port
                    )
                    self.api_base_url = base_url + 'api/'
                    self.access_token_url = base_url + 'oauth/token'
                    self.authorize_url = base_url + 'oauth/authorize'
                    p = requests.post(url=self.access_token_url, data=data,
                                      verify=False, timeout=10)

                if p.status_code == 401:
                    return json.dumps(
                        {'status': False, 'msg': 'API authentication failed'})
                else:
                    self.access_token = p.json().get('access_token')
                    self.refresh_token = p.json().get('refresh_token')
                    self.remote_oauth = (self.access_token, self.refresh_token)
                    return json.dumps(
                        {'status': True, 'msg': 'API access granted'})

            # todo : to be tested + manage https and private/public IP address
            elif self.method.lower() == "grant_code":
                url = self.authorize_url + '?client_id=' + self.client_id + \
                      "&response_type=code"
                driver = webdriver.Firefox()
                return driver.get(url)
            else:
                return json.dumps(
                    {'status': False, 'msg': 'Invalid grant type'})

        except Exception as e:
            self.log.error('get_access_token Exception : {0}'.format(e))
            return json.dumps(
                {'status': False, 'msg': 'API authentication failed'})

    """
    Everything related to the user
    """

    def get_user_profile(self):
        try:
            p = self.generic_request(url=self.api_base_url + 'user/profile',
                                     method='GET')
        except Exception as e:
            self.log.error('get_user_profile Exception : {0}'.format(e))
            return json.dumps('Get user profile : Bad request')
        return p

    def update_user_profile(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'user/profile',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('update_user_profile Exception : {0}'.format(e))
            return json.dumps('Update user profile : Bad request')
        return p

    def delete_custom_profile_item(self, data):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'user/profile/delete_item',
                method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error(
                'delete_custom_profile_item Exception : {0}'.format(e))
            return json.dumps('Delete custom profile item : Bad request')
        return p

    def get_user_avatar(self):
        try:
            p = self.generic_request(url=self.api_base_url + 'user/avatar',
                                     method='GET')
        except Exception as e:
            self.log.error('get_user_avatar Exception : {0}'.format(e))
            return json.dumps('Get user avatar : Bad request')
        return p

    def set_user_avatar(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'user/avatar',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('set_user_avatar Exception : {0}'.format(e))
            return json.dumps('Update user avatar : Bad request')
        return p

    def update_password(self, data):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'profile/change_password',
                method='POST',
                params=json.dumps(data))
        except Exception as e:
            self.log.error('update_password Exception : {0}'.format(e))
            return json.dumps('Update password : Bad request')
        return p

    """
    Everything related to chat messages
    """

    def send_chat_message(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'chat/send',
                                     method="POST", params=json.dumps(data))
        except Exception as e:
            self.log.error('send_chat_message Exception : {0}'.format(e))
            return json.dumps('Send chat message : Bad request')
        return p

    def delete_chat_message(self, msg_id):
        try:
            p = self.generic_request(url=self.api_base_url + 'chat/' + msg_id,
                                     method="DELETE")
        except Exception as e:
            self.log.error('delete_chat_message Exception : {0}'.format(e))
            return json.dumps('Delete chat message : Bad request')
        return p

    def get_chat_conversation(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'chat',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('get_chat_conversation Exception : {0}'.format(e))
            return json.dumps('Get chat conversation : Bad request')
        return p

    """
    Everything related to file messages
    """

    def get_file_messages(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'file_message',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('get_file_messages Exception : {0}'.format(e))
            return json.dumps('Get file messages : Bad request')
        return p

    def send_file_message(self, data):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'file_message/send',
                method="POST",
                params=json.dumps(data))
        except Exception as e:
            self.log.error('send_file_message Exception : {0}'.format(e))
            return json.dumps('Send file message : Bad request')
        return p

    def delete_file_message(self, msg_id):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'file_message/' + msg_id,
                method='DELETE')
        except Exception as e:
            self.log.error('delete_file_message Exception : {0}'.format(e))
            return json.dumps('Set file message as read : Bad request')
        return p

    """
    Everything related to contacts
    """

    def get_contacts(self):
        try:
            p = self.generic_request(url=self.api_base_url + 'contacts',
                                     method='GET')
        except Exception as e:
            self.log.error('get_contacts Exception : {0}'.format(e))
            return json.dumps(
                'Get contacts list : Bad request : {0}'.format(e))
        return p

    def find_user(self, query):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'contacts/find_user' + query,
                method='GET')
        except Exception as e:
            self.log.error('find_user Exception : {0}'.format(e))
            return json.dumps('Find user : Bad request')
        return p

    def add_contact(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'contacts/add',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('add_contact Exception : {0}'.format(e))
            return json.dumps('Add contact : Bad request')
        return p

    def remove_contact(self, data):
        try:
            p = self.generic_request(url=self.api_base_url + 'contacts/remove',
                                     method='POST', params=json.dumps(data))
        except Exception as e:
            self.log.error('remove_contact Exception : {0}'.format(e))
            return json.dumps('Remove contact : Bad request')
        return p

    def accept_contact_request(self, matr_id):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'contacts/accept/' + matr_id,
                method='GET')
        except Exception as e:
            self.log.error('accept_contact_request Exception : {0}'.format(e))
            return json.dumps('Accept contact request : Bad request')
        return p

    def reject_contact_request(self, matr_id):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'contacts/reject/' + matr_id,
                method='GET')
        except Exception as e:
            self.log.error('reject_contact_request Exception : {0}'.format(e))
            return json.dumps('Reject contact request : Bad request')
        return p

    def get_contact_profile(self, matr_id):
        try:
            p = self.generic_request(
                url=self.api_base_url + 'contacts/' + matr_id, method='GET')
        except Exception as e:
            self.log.error('get_contact_profile Exception : {0}'.format(e))
            return json.dumps('Get contact profile : Bad request')
        return p
