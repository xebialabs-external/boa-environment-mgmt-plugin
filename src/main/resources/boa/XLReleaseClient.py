#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import urllib

from distutils.version import LooseVersion
from boa.HttpClient import HttpClient

class XLReleaseClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpClient(http_connection, username, password)

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return XLReleaseClient(http_connection, username, password)

    @staticmethod
    def get_release_url(release_id):
        return release_id.replace("Applications/","").replace("/","-")

    def get_version(self):
        xlr_api_url = '/server/info'
        xlr_response = self.http_request.get_request(
            xlr_api_url, additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        data = xlr_response.json()
        return data["version"]

    def _is_using_filter(self):
        return LooseVersion(self.get_version()) < LooseVersion("7.2.0")

    def get_stage_id(self, stage_title):
        xlr_api_url = '/api/v1/environments/stages/search'
        content = {"title": stage_title}
        xlr_response = self.http_request.post_request(xlr_api_url, json.dumps(content),
                                                      additional_headers={"Accept": "application/json",
                                                                          "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Response for search Stage %s\n" % stage_title
        data = xlr_response.json()
        return data[0]["id"]

    def get_env_id(self, env_title,stage_title):
        xlr_api_url = '/api/v1/environments/search'
        content = """{"title":"%s","stage":"%s"}""" % (env_title, stage_title)
        print content
        xlr_response = self.http_request.post_request(xlr_api_url, content,
                                                      additional_headers={"Accept": "application/json",
                                                                          "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Response for search Stage %s\n" % stage_title
        data = xlr_response.json()
        return data[0]["id"]
