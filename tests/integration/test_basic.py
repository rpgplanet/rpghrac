# -*- coding: utf-8 -*-
from djangosanetesting import HttpTestCase
from djangosanetesting.utils import mock_settings, get_live_server_path

from urllib2 import urlopen, HTTPError

from rpgcommon.user.user import create_user

class TestUserSubdomainsForcable(HttpTestCase):
    def test_without_fixture_there_is_no_site_in_root(self):
        try:
            res = urlopen(get_live_server_path())
        except HTTPError, e:
            self.assert_equals(404, e.code)
        else:
            self.fail("404 expected")

    @mock_settings("RPGHRAC_FORCE_USER_SUBDOMAIN_TO", "tester")
    def test_subdomain_not_available_without_user(self):
        self.test_without_fixture_there_is_no_site_in_root()

    @mock_settings("RPGHRAC_FORCE_USER_SUBDOMAIN_TO", "tester")
    def test_available_to_created_and_forced(self):
        create_user("tester", "xxx", "tester@example.com")
        self.transaction.commit()

        res = urlopen(get_live_server_path())
        self.assert_equals(200, res.code)
        