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

import random
import uuid

from keystoneauth1 import exceptions
from keystoneauth1 import loading
from keystoneauth1.tests.unit.loading import utils


class V3PasswordTests(utils.TestCase):

    def setUp(self):
        super(V3PasswordTests, self).setUp()

        self.auth_url = uuid.uuid4().hex

    def create(self, **kwargs):
        kwargs.setdefault('auth_url', self.auth_url)
        loader = loading.get_plugin_loader('v3password')
        return loader.load_from_options(**kwargs)

    def test_basic(self):
        username = uuid.uuid4().hex
        user_domain_id = uuid.uuid4().hex
        password = uuid.uuid4().hex
        project_name = uuid.uuid4().hex
        project_domain_id = uuid.uuid4().hex

        p = self.create(username=username,
                        user_domain_id=user_domain_id,
                        project_name=project_name,
                        project_domain_id=project_domain_id,
                        password=password)

        pw_method = p.auth_methods[0]

        self.assertEqual(username, pw_method.username)
        self.assertEqual(user_domain_id, pw_method.user_domain_id)
        self.assertEqual(password, pw_method.password)

        self.assertEqual(project_name, p.project_name)
        self.assertEqual(project_domain_id, p.project_domain_id)

    def test_without_user_domain(self):
        self.assertRaises(exceptions.OptionError,
                          self.create,
                          username=uuid.uuid4().hex,
                          password=uuid.uuid4().hex)

    def test_without_project_domain(self):
        self.assertRaises(exceptions.OptionError,
                          self.create,
                          username=uuid.uuid4().hex,
                          password=uuid.uuid4().hex,
                          user_domain_id=uuid.uuid4().hex,
                          project_name=uuid.uuid4().hex)


class TOTPTests(utils.TestCase):

    def setUp(self):
        super(TOTPTests, self).setUp()

        self.auth_url = uuid.uuid4().hex

    def create(self, **kwargs):
        kwargs.setdefault('auth_url', self.auth_url)
        loader = loading.get_plugin_loader('v3totp')
        return loader.load_from_options(**kwargs)

    def test_basic(self):
        username = uuid.uuid4().hex
        user_domain_id = uuid.uuid4().hex
        # passcode is 6 digits
        passcode = ''.join(str(random.randint(0, 9)) for x in range(6))
        project_name = uuid.uuid4().hex
        project_domain_id = uuid.uuid4().hex

        p = self.create(username=username,
                        user_domain_id=user_domain_id,
                        project_name=project_name,
                        project_domain_id=project_domain_id,
                        passcode=passcode)

        totp_method = p.auth_methods[0]

        self.assertEqual(username, totp_method.username)
        self.assertEqual(user_domain_id, totp_method.user_domain_id)
        self.assertEqual(passcode, totp_method.passcode)

        self.assertEqual(project_name, p.project_name)
        self.assertEqual(project_domain_id, p.project_domain_id)

    def test_without_user_domain(self):
        self.assertRaises(exceptions.OptionError,
                          self.create,
                          username=uuid.uuid4().hex,
                          passcode=uuid.uuid4().hex)

    def test_without_project_domain(self):
        self.assertRaises(exceptions.OptionError,
                          self.create,
                          username=uuid.uuid4().hex,
                          passcode=uuid.uuid4().hex,
                          user_domain_id=uuid.uuid4().hex,
                          project_name=uuid.uuid4().hex)


class OpenIDConnectBaseTests(object):

    plugin_name = None

    def setUp(self):
        super(OpenIDConnectBaseTests, self).setUp()

        self.auth_url = uuid.uuid4().hex

    def create(self, **kwargs):
        kwargs.setdefault('auth_url', self.auth_url)
        loader = loading.get_plugin_loader(self.plugin_name)
        return loader.load_from_options(**kwargs)

    def test_base_options_are_there(self):
        options = loading.get_plugin_loader(self.plugin_name).get_options()
        self.assertTrue(
            set(['client-id', 'client-secret', 'access-token-endpoint',
                 'access-token-type']).issubset(
                     set([o.name for o in options]))
        )


class OpenIDConnectPasswordTests(OpenIDConnectBaseTests, utils.TestCase):

    plugin_name = "v3oidcpassword"

    def test_options(self):
        options = loading.get_plugin_loader(self.plugin_name).get_options()
        self.assertTrue(
            set(['username', 'password', 'openid-scope']).issubset(
                set([o.name for o in options]))
        )

    def test_basic(self):
        access_token_endpoint = uuid.uuid4().hex
        username = uuid.uuid4().hex
        password = uuid.uuid4().hex
        scope = uuid.uuid4().hex
        identity_provider = uuid.uuid4().hex
        protocol = uuid.uuid4().hex
        client_id = uuid.uuid4().hex
        client_secret = uuid.uuid4().hex

        oidc = self.create(username=username,
                           password=password,
                           identity_provider=identity_provider,
                           protocol=protocol,
                           access_token_endpoint=access_token_endpoint,
                           client_id=client_id,
                           client_secret=client_secret,
                           scope=scope)

        self.assertEqual(username, oidc.username)
        self.assertEqual(password, oidc.password)
        self.assertEqual(identity_provider, oidc.identity_provider)
        self.assertEqual(protocol, oidc.protocol)
        self.assertEqual(access_token_endpoint, oidc.access_token_endpoint)
        self.assertEqual(client_id, oidc.client_id)
        self.assertEqual(client_secret, oidc.client_secret)


class OpenIDConnectAuthCodeTests(OpenIDConnectBaseTests, utils.TestCase):

    plugin_name = "v3oidcauthcode"

    def test_options(self):
        options = loading.get_plugin_loader(self.plugin_name).get_options()
        self.assertTrue(
            set(['redirect-uri', 'authorization-code']).issubset(
                set([o.name for o in options]))
        )

    def test_basic(self):
        access_token_endpoint = uuid.uuid4().hex
        redirect_uri = uuid.uuid4().hex
        authorization_code = uuid.uuid4().hex
        identity_provider = uuid.uuid4().hex
        protocol = uuid.uuid4().hex
        client_id = uuid.uuid4().hex
        client_secret = uuid.uuid4().hex

        oidc = self.create(code=authorization_code,
                           redirect_uri=redirect_uri,
                           identity_provider=identity_provider,
                           protocol=protocol,
                           access_token_endpoint=access_token_endpoint,
                           client_id=client_id,
                           client_secret=client_secret)

        self.assertEqual(redirect_uri, oidc.redirect_uri)
        self.assertEqual(authorization_code, oidc.code)
        self.assertEqual(identity_provider, oidc.identity_provider)
        self.assertEqual(protocol, oidc.protocol)
        self.assertEqual(access_token_endpoint, oidc.access_token_endpoint)
        self.assertEqual(client_id, oidc.client_id)
        self.assertEqual(client_secret, oidc.client_secret)


class OpenIDConnectAccessToken(utils.TestCase):

    plugin_name = "v3oidcaccesstoken"

    def setUp(self):
        super(OpenIDConnectAccessToken, self).setUp()

        self.auth_url = uuid.uuid4().hex

    def create(self, **kwargs):
        kwargs.setdefault('auth_url', self.auth_url)
        loader = loading.get_plugin_loader(self.plugin_name)
        return loader.load_from_options(**kwargs)

    def test_options(self):
        options = loading.get_plugin_loader(self.plugin_name).get_options()
        self.assertTrue(
            set(['access-token']).issubset(
                set([o.name for o in options]))
        )

    def test_basic(self):
        access_token = uuid.uuid4().hex
        identity_provider = uuid.uuid4().hex
        protocol = uuid.uuid4().hex

        oidc = self.create(access_token=access_token,
                           identity_provider=identity_provider,
                           protocol=protocol)

        self.assertEqual(identity_provider, oidc.identity_provider)
        self.assertEqual(protocol, oidc.protocol)
        self.assertEqual(access_token, oidc.access_token)
