#!/usr/bin/env python

import os
import sys
import argparse
import unittest


myPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))
from check_novaapi import *



###### Test Object ######

######### Success ##########
class FlavorsTestSuccess(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ("flavor1","flavor2","flavor3")

class ServersTestSuccess(object):
    def __init__(self):
        pass
    def list(self):
        return ("servers1","servers2","servers3")

class ImagesTestSuccess(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ("images1","images2","images3")

class Security_groupsTestSuccess(object):
    def __init__(self):
        pass
    def list(self):
        return ("images1","images2","images3")

class ClientTestSuccess(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestSuccess()
    servers=ServersTestSuccess()
    images=ImagesTestSuccess()
    security_groups=Security_groupsTestSuccess()

######### Flavors fail ##########

class FlavorsTestFail(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ()

class ClientTestFlavorsFail(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestFail()
    servers=ServersTestSuccess()
    images=ImagesTestSuccess()
    security_groups=Security_groupsTestSuccess()

######### Servers fail ##########

class ServersTestFail(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ()

class ClientTestServersFail(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestSuccess()
    servers=ServersTestFail()
    images=ImagesTestSuccess()
    security_groups=Security_groupsTestSuccess()

######### Images fail ##########

class ImagesTestFail(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ()

class ClientTestImagesFail(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestSuccess()
    servers=ServersTestSuccess()
    images=ImagesTestFail()
    security_groups=Security_groupsTestSuccess()

######### Security_groups fail ##########

class Security_groupsTestFail(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ()

class ClientTestSecurity_groupsFail(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestSuccess()
    servers=ServersTestSuccess()
    images=ImagesTestSuccess()
    security_groups=Security_groupsTestFail()


#########  Flavors and images fail ##########

class Security_groupsTestFail(object):
    def __init__(self):
        pass
    def list(self, detailed=False):
        return ()

class ClientTestFlavors_ImagesFail(object):
    def __init__(self,username, password, tenant, auth_url, service_type):
        self.username = username
        self.password = password
        self.tenant = tenant
        self.auth_url = auth_url
        self.service_type = service_type

    flavors=FlavorsTestFail()
    servers=ServersTestSuccess()
    images=ImagesTestFail()
    security_groups=Security_groupsTestSuccess()


args = collect_args().parse_args(['--auth_url', 'http://beta.enocloud.com:5000/v2.0/', '--username', 'admin', '--password', 'p4st0uch3', '--tenant', 'admin'])

class NovaApiTestCase(unittest.TestCase):
    def get_init(self):
      pass

    def setUp(self):
      global RETURN_STATE
      RETURN_STATE = 0
      global STATE_MESSAGE
      STATE_MESSAGE = ""
    
    def tearDown(self):
      pass
    
    def test_success(self):
      nt = ClientTestSuccess(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      check_novaapi(nt)

    def test_flavors_fail(self):
      nt = ClientTestFlavorsFail(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      check_novaapi(nt)

    def test_servers_fail(self):
      nt = ClientTestServersFail(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      check_novaapi(nt)

    def test_images_fail(self):
      nt = ClientTestImagesFail(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      check_novaapi(nt)

    def test_security_groups_fail(self):
      nt = ClientTestSecurity_groupsFail(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      check_novaapi(nt)

    def test_flavors_images_fail(self):
      nt = ClientTestFlavors_ImagesFail(args.username,
             args.password,
             args.tenant,
             args.auth_url,
             service_type="compute")
      try:
        check_novaapi(nt)
      except SystemExit:
        self.assertTrue("two warning raised SystemExit")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(NovaApiTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)
