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
import sys
from datetime import date

from boa.XLReleaseClientUtil import XLReleaseClientUtil

APPLICATION_CREATED_STATUS = 200
APPLICATION_FOUND_STATUS = 200
ENVIRONMENT_FOUND_STATUS = 200

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlrUrl = xlrServer['url']
xlrUrl = xlrUrl.rstrip("/")

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

xlr_client = XLReleaseClientUtil.create_xl_release_client(xlrServer, username, password)

xlrAPIUrl = xlrUrl + '/api/v1/applications'

#Get Release variables.
vars = getCurrentRelease().getVariables()

typeMap = {}
stage = ""
environments = []
spk = ''
applications = []

for var in vars:
    if var.key == releaseEnvironment:
        environments = var.value
    elif var.key == envNameToEnvTypeMapping:
        typeMap = var.value
    elif var.key == spkName:
        spk = var.value
    elif var.key == spkComponentsToRelease:
        applications = var.value

xlrEnvList = []
for env in environments:
    xlrEnvList.append(env + '-'+ spk)

for app in applications:
    #Check if app is already there.
    content = {"title": app, "environments": xlrEnvList}

    print content

    xlrResponse = XLRequest(xlrAPIUrl+'/search', 'POST', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

    if xlrResponse.status == APPLICATION_FOUND_STATUS:
        data = json.loads(xlrResponse.read())
        if not len(data) == 0:
            appId = data[0]["id"]
            print "Found App %s in XLR" % (appId)
            continue
    else:
        print "Failed to find app in XLR"
        xlrResponse.errorDump()
        sys.exit(1)

    # Get environment IDs
    envIds = []
    for env in environments:
        envSearchAPIUrl = xlrUrl + '/api/v1/environments/search'
        stage = typeMap[env]

        envTitle = env + '-'+ spk
        #Check if environment is already there.
        content = """{"title":"%s","stage":"%s"}""" % (envTitle, stage)

        xlrResponse = XLRequest(envSearchAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

        if xlrResponse.status == ENVIRONMENT_FOUND_STATUS:
            data = json.loads(xlrResponse.read())
            if not len(data) == 0:
                envId = data[0]["id"]
                print "Found Env %s in XLR" % (envId)
                envIds.append(envId)
        else:
            print "Failed to find environment in XLR"
            xlrResponse.errorDump()
            sys.exit(1)


    #Create App
    content = {"title": app, "environmentIds": envIds}

    print xlrAPIUrl
    print content

    xlrResponse = XLRequest(xlrAPIUrl, 'POST', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

    envId = None
    if xlrResponse.status == APPLICATION_CREATED_STATUS:
        data = json.loads(xlrResponse.read())
        appId = data["id"]
        print "Created %s in XLR" % (appId)
    else:
        print "Failed to create App in XLR"
        xlrResponse.errorDump()
        sys.exit(1)
