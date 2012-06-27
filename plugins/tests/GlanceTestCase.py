#!/usr/bin/env python
#
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Florian Lambert <florian.lambert@enovance.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import argparse
import unittest


myPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from check_glance import *


###### Test Object ######

######### Success ##########
class GlanceClientTestSuccess(object):
    def __init__(self, host, username, password, tenant, auth_url, region="default"):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.region = region

    def get_images(self,**parameters):
        try:
          if(parameters["filters"]["name"]):
            return [parameters["filters"]["name"]]
        except :
          pass
        return ("Debian GNU/Linux 6.0.4 amd64","images2","turnkey-wordpress-11.3-lucid-x86")

######### Images fail ##########

######### Success ##########
class GlanceClientTestImagesFail(object):
    def __init__(self, host, username, password, tenant, auth_url, region="default"):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.region = region

    def get_images(self,**parameters):
        try:
          if(parameters["filters"]["name"]):
            return ()
        except :
          pass
        return ("Debian GNU/Linux 6.0.4 amd64","images2","turnkey-wordpress-11.3-lucid-x86")



class GlanceTestCase(unittest.TestCase):
    def get_init(self):
      pass

    def setUp(self):
      global RETURN_STATE
      RETURN_STATE = 0
      global STATE_MESSAGE
      STATE_MESSAGE = ""

    def tearDown(self):
      pass

    def test_connection_success(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin'])
      c = GlanceClientTestSuccess(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      check_glance(c,args)

    def test_limit_success(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_count', '2'])
      c = GlanceClientTestSuccess(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      check_glance(c,args)

    def test_limit_fail(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_count', '10'])
      c = GlanceClientTestSuccess(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      try:
        check_glance(c,args)
      except SystemExit:
        self.assertTrue("not enough images")

    def test_images_success(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_images','Debian GNU/Linux 6.0.4 amd64','turnkey-wordpress-11.3-lucid-x86'])
      c = GlanceClientTestSuccess(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      check_glance(c,args)

    def test_images_fail(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_images','Debian GNU/Linux 6.0.4 amd64','turnkey-wordpress-11.3-lucid-x86'])
      c = GlanceClientTestImagesFail(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      try:
        check_glance(c,args)
      except SystemExit:
        self.assertTrue("images not found")


    def test_images_limit_fail(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_count', '10','--req_images','Debian GNU/Linux 6.0.4 amd64','turnkey-wordpress-11.3-lucid-x86'])
      c = GlanceClientTestImagesFail(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      try:
        check_glance(c,args)
      except SystemExit:
        self.assertTrue("images not found")

    def test_images_limit_success(self):
      args = collect_args().parse_args(['--host','beta.enocloud.com','--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin', '--req_count', '2', '--req_images','Debian GNU/Linux 6.0.4 amd64','turnkey-wordpress-11.3-lucid-x86'])
      c = GlanceClientTestSuccess(args.host,
              args.username,
              args.password,
              args.tenant,
              args.auth_url,
              args.region_name)
      check_glance(c,args)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(GlanceTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)
