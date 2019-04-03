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
APPLICATION_UPDATED_STATUS = 200

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

# Create env lists for api calls

xlrEnvList = []
xlrEnvIdList = []
for env in environments:
    envTitle = spk.upper() + '-'+ env.upper()
    xlrEnvList.append(envTitle)
    # Get environment IDs
    stage = typeMap[env]
    envId = xlr_client.get_env_id(envTitle,stage)
    xlrEnvIdList.append(envId)


for app in applications:
    #Check if app is already there.
    content = {"title": app}
    foundApp = False

    xlrResponse = XLRequest(xlrAPIUrl+'/search', 'POST', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

    if xlrResponse.status == APPLICATION_FOUND_STATUS:
        data = json.loads(xlrResponse.read())
        if not len(data) == 0:
            for idx,appElement in enumerate(data):
                appId = appElement["id"]
                existingAppTitle = appElement["title"]
                if app == existingAppTitle:
                    print "Found App %s in XLR" % (appId)
                    foundApp = True

                    # Create env list with the new environments.
                    envCompositeList = appElement["environments"]
                    existingEnvList = []
                    for e in envCompositeList:
                        existingEnvList.append(e["id"])

                    deltaList = list(set(xlrEnvIdList +existingEnvList))
                    if len(deltaList) == 0:
                        continue
                    else:
                    #Update the app with new env
                        content = {"title": app, "environmentIds": deltaList}

                        xlrResponse = XLRequest(xlrAPIUrl+'/'+appId, 'PUT', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

                        if xlrResponse.status == APPLICATION_UPDATED_STATUS:
                            data = json.loads(xlrResponse.read())
                            appId = data["id"]
                            print "Updated %s in XLR" % (appId)
                            continue
                        else:
                            print "Failed to update App in XLR"
                            xlrResponse.errorDump()
                            sys.exit(1)
    else:
        print "Failed to find app in XLR"
        xlrResponse.errorDump()
        sys.exit(1)



    #Create App
    if not foundApp:
        content = {"title": app, "environmentIds": xlrEnvIdList}


        xlrResponse = XLRequest(xlrAPIUrl, 'POST', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

        if xlrResponse.status == APPLICATION_CREATED_STATUS:
            data = json.loads(xlrResponse.read())
            appId = data["id"]
            print "Created %s in XLR" % (appId)
        else:
            print "Failed to create App in XLR"
            xlrResponse.errorDump()
            sys.exit(1)
