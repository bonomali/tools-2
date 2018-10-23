
import requests
from requests.auth import HTTPBasicAuth
# import pprint
import json
import sys
import os
import collections
import shutil
import pprint
import string
import random
import urllib3

def parse_response(response):
    parsed_json = json.loads(response)
    if parsed_json["errors"]:
        for value in parsed_json["messages"]:
            print "Error: " + value["messageText"]
        return False

    return True

def reset_blueprints(URL, username, password):
    print "Resetting all Blueprints"

    if URL.endswith('/'):
        request_url = URL + 'api/blueprints/'
    else:
        request_url = URL + '/api/blueprints/'

    req = requests.get(request_url + 'filter?page=0&pageSize=10000&q=MY', auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text
    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        delete_url = request_url + value['id']
        print "Deleting BluePrint: " + delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        if not parse_response(req.text):
            print "Error Deleting BluePrint: " + delete_url 



def reset_plugins(URL, username, password):
    print "Resetting all Plugins"
    if URL.endswith('/'):
        request_url = URL + 'api/plugins/'
    else:
        request_url = URL + '/api/plugins/'

    req = requests.get(request_url + 'manage?page=0&pageSize=10000', auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        delete_url = request_url + value['id']
        print "Deleting Plugins: " + delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        if not parse_response(req.text):
            print "Error Deleting Plugins: " + delete_url

def reset_tenants(URL, username, password):
    print "Resetting all tenants"
    if URL.endswith('/'):
        request_url = URL + 'api/tenants/'
    else:
        request_url = URL + '/api/tenants/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        print "Deleting Tenant: " + value['email']
        reset_tenant(URL, username, password, value['email'])
        # req = requests.delete(request_url, auth=HTTPBasicAuth(username, password), verify=False)
        # response = req.text

def reset_tenant(URL, username, password, email_id):
    print "Resetting all tenant: " + email_id
    if URL.endswith('/'):
        request_url = URL + 'api/users/'
    else:
        request_url = URL + '/api/users/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        if value['email'] == email_id:
            tenant_user_id = value['id']
            tenant_password = "test1234"
            value['password'] = tenant_password
            if URL.endswith('/'):
                request_url = URL + 'api/users/' + tenant_user_id
            else:
                request_url = URL + '/api/users/' + tenant_user_id
            body = json.dumps(value)
            print "Tenant Admin is: " + tenant_user_id
            print "Changing Tenant Admin Password"
            # response = requests.post(request_url, auth=HTTPBasicAuth(username, password), verify=False, data=body)
            reset_tenant_containers(URL, tenant_user_id, tenant_password)
            # reset_tenant_clusters(URL, tenant_user_id, tenant_password)
            # reset_tenant_vms(URL, tenant_user_id, tenant_password)
            # reset_tenant_resourcepools(URL, tenant_user_id, tenant_password)

def reset_tenant_containers(URL, username, password):
    print "Resetting all tenant container"
    if URL.endswith('/'):
        request_url = URL + 'api/provision/active/'
    else:
        request_url = URL + '/api/provision/active/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        container_id = value['id']

        if URL.endswith('/'):
            request_url = URL + 'api/provision/' + container_id
        else:
            request_url = URL + '/api/provision/' + container_id
        req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text

        parsed_json = json.loads(response)
        results = parsed_json['results']

        if URL.endswith('/'):
            request_url = URL + 'api/provision/' + container_id + '/destroy/true'
        else:
            request_url = URL + '/api/provision/' + container_id + '/destroy/true'
        #body = json.dumps(results)
        print "Deleting Containers"
        print request_url
        # response = requests.post(request_url, auth=HTTPBasicAuth(username, password), verify=False, data=body)
        # response = req.text

# def reset_tenant_clusters(URL, username, password):
#     #
#
# def reset_tenant_vms(URL, username, password):
#     #
#
# def reset_tenant_resourcepools(URL, username, password):
#     #

def random_passwordgenerator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

def reset_onprem_providers(URL, username, password):
    print "Resetting on premise provider"
    if URL.endswith('/'):
        request_url = URL + 'api/registryaccounts/'
    else:
        request_url = URL + '/api/registryaccounts/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        if (value['accountType'] == "HYPER_GRID") or (value['accountType'] == "HCS_VSPHERE") or (value['accountType'] == "VLAN_PROVIDER"):
            print value['accountType']
            delete_url = request_url + value['id']
            print delete_url
            # req = requests.delete(request_url, auth=HTTPBasicAuth(username, password), verify=False)
            # response = req.text

def reset_public_providers(URL, username, password):
    if URL.endswith('/'):
        request_url = URL + 'api/registryaccounts/'
    else:
        request_url = URL + '/api/registryaccounts/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        if (value['accountType'] != "HYPER_GRID") and (value['accountType'] != "HCS_VSPHERE") and (value['accountType'] != "VLAN_PROVIDER"):
            print value['accountType']
            delete_provider_url = request_url + value['id']
            print delete_provider_url

            availability_zones_request_url = request_url + 'azs/' + value['id']
            req = requests.get(availability_zones_request_url, auth=HTTPBasicAuth(username, password), verify=False)
            az_response = req.text

            parsed_json = json.loads(az_response)
            az_results = parsed_json['results']

            for az_value in az_results:
                print "Availability Zones:"
                print az_value['id']
                delete_availability_zone_url = request_url + az_value['id']

            # req = requests.delete(request_url, auth=HTTPBasicAuth(username, password), verify=False)
            # response = req.text

def reset_az_for_provider(URL, username, password, az_id):
    if URL.endswith('/'):
        request_url = URL + 'api/registryaccounts/azs/'
    else:
        request_url = URL + '/api/registryaccounts/azs/'

    request_url = request_url + az_id + '?page=0&pageSize=10000'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    
    for value in results:
        if URL.endswith('/'):
            delete_url = URL + 'api/registryaccounts/'
        else:
            delete_url = URL + '/api/registryaccounts/'
        delete_url = delete_url + value['id']
        print delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        print response

def reset_all_providers(URL, username, password):
    if URL.endswith('/'):
        request_url = URL + 'api/registryaccounts/'
    else:
        request_url = URL + '/api/registryaccounts/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        print value['accountType']
        reset_az_for_provider(URL, username, password, value['id'])
        delete_url = request_url + value['id']
        print delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        print response

def setup_aws(url, username, password, aws_accountname, aws_username, aws_password, aws_groupname):
    print "Setting up AWS account: " + aws_accountname
    if url.endswith('/'):
        request_url = url + 'api/registryaccounts/'
    else:
        request_url = url + '/api/registryaccounts/'
    new_provider_data = collections.OrderedDict()
    new_provider_data["inactive"] = False
    new_provider_data["entitlementType"]="OWNER"
    new_provider_data["blueprintEntitlementType"] = "ALL_BLUEPRINTS"
    new_provider_data["groupName"] = aws_groupname
    new_provider_data["vmQuota"] = 100
    new_provider_data["freeFormEntitlement"] = True
    new_provider_data["approvalEnforced"] = False
    new_provider_data["username"] = aws_username
    new_provider_data["password"] = aws_password
    new_provider_data["name"] = aws_accountname
    new_provider_data["prefix"] = aws_accountname.split(".")[0] + "." + aws_accountname.split(".")[1] + "."
    new_provider_data["region"] = aws_accountname.split(".")[1]
    new_provider_data["accountType"] = "AWS_EC2"
    body = json.dumps(new_provider_data)
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if not parse_response(req.text):
        print "Error Setting up AWS account: " + aws_accountname


def setup_gcp(url, username, password, gcp_accountname, gcp_email, gcp_json, gcp_groupname):
    print "Setting up GCP account: " + gcp_accountname
    if url.endswith('/'):
        request_url = url + 'api/registryaccounts/'
    else:
        request_url = url + '/api/registryaccounts/'
    new_provider_data = collections.OrderedDict()
    new_provider_data["inactive"] = False
    new_provider_data["entitlementType"]="OWNER"
    new_provider_data["blueprintEntitlementType"] = "ALL_BLUEPRINTS"
    new_provider_data["groupName"] = gcp_groupname
    new_provider_data["vmQuota"] = 100
    new_provider_data["freeFormEntitlement"] = True
    new_provider_data["approvalEnforced"] = False
    new_provider_data["username"] = gcp_email
    new_provider_data["password"] = gcp_json
    new_provider_data["name"] = gcp_accountname
    new_provider_data["prefix"] = gcp_accountname.split(".")[0] + "." + gcp_accountname.split(".")[1] + "."
    new_provider_data["region"] = gcp_accountname.split(".")[1]
    new_provider_data["accountType"] = "GOOGLE_COMPUTE_ENGINE"
    body = json.dumps(new_provider_data)
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if not parse_response(req.text):
        print "Error Setting up GCP account: " + gcp_accountname

def setup_azure(url, username, password, azure_accountname, azure_email, azure_url, azure_username, azure_password, azure_groupname):
    print "Setting up Azure account: " + azure_accountname
    if url.endswith('/'):
        request_url = url + 'api/registryaccounts/'
    else:
        request_url = url + '/api/registryaccounts/'
    new_provider_data = collections.OrderedDict()
    new_provider_data["inactive"] = False
    new_provider_data["entitlementType"]="OWNER"
    new_provider_data["blueprintEntitlementType"] = "ALL_BLUEPRINTS"
    new_provider_data["groupName"] = azure_groupname
    new_provider_data["vmQuota"] = 100
    new_provider_data["freeFormEntitlement"] = True
    new_provider_data["approvalEnforced"] = False
    new_provider_data["username"] = azure_username
    new_provider_data["password"] = azure_password
    new_provider_data["email"] = azure_email
    new_provider_data["url"] = azure_url
    new_provider_data["name"] = azure_accountname
    new_provider_data["prefix"] = azure_accountname.split(".")[0] + "." + azure_accountname.split(".")[1] + "."
    new_provider_data["region"] = azure_accountname.split(".")[1]
    new_provider_data["accountType"] = "MICROSOFT_ARM"
    body = json.dumps(new_provider_data)
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if not parse_response(req.text):
        print "Error Setting up Azure account: " + azure_accountname

def setup_plugins(url, username, password, plugin_dir):
    print "Setting up Plugins"
    if url.endswith('/'):
        request_url = url + 'api/plugins/'
    else:
        request_url = url + '/api/plugins/'
    plugin_files = os.listdir(plugin_dir)
    for file in plugin_files:
        
        new_plugin_data = collections.OrderedDict()
        new_plugin_data["editable"] = True
        new_plugin_data["inactive"] = False
        new_plugin_data["referenceId"] = ""
        new_plugin_data["name"] = ""
        new_plugin_data["license"] = ""
        new_plugin_data["description"] = ""
        new_plugin_data["baseScript"] = ""
        new_plugin_data["envs"] = ""
        new_plugin_data["scriptArgs"] = ""
        new_plugin_data["entitlementType"] = "GLOBAL"

        with open(plugin_dir+"/"+file) as json_file:
            plugin_build = json.load(json_file)
            for key, value in new_plugin_data.items():
                if value == "":
                    for search_key, search_value in plugin_build.items():
                        if search_key == key:
                            search_key = search_key.encode("utf-8")
                            if isinstance(search_value, list):
                                a = 0
                            elif isinstance(search_value, type(None)):
                                a = 0
                            else:
                                search_value = search_value.encode("utf-8")
                            new_plugin_data[key] = search_value
        print "Inserting Plugin: " + new_plugin_data["name"]
        body = json.dumps(new_plugin_data)
        headers = {'Content-Type': 'application/json'}
        req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
        if not parse_response(req.text):
            print "Error Inserting Plugin: " + new_plugin_data["name"]

def setup_blueprints(url, username, password, blueprint_dir):
    print "Setting up Blueprints"
    if url.endswith('/'):
        request_url = url + 'api/blueprints/'
    else:
        request_url = url + '/api/blueprints/'
    blueprint_files = os.listdir(blueprint_dir)
    for file in blueprint_files:
        new_blueprint_data = collections.OrderedDict()
        new_blueprint_data["editable"] = True
        new_blueprint_data["inactive"] = False
        new_blueprint_data["blueprintType"] = "DOCKER_COMPOSE"
        new_blueprint_data["imageLink"] = ""
        new_blueprint_data["images"] = []
        new_blueprint_data["entitlementType"] = "GLOBAL"
        new_blueprint_data["serviceTypes"] = []
        new_blueprint_data["version"] = ""
        new_blueprint_data["visibility"] = ""
        new_blueprint_data["licenseModel"] = "LICENSE_INCLUDED"
        new_blueprint_data["yml"] = ""
        new_blueprint_data["params"] = ""
        new_blueprint_data["composeVersion"] = "V1"
        new_blueprint_data["name"] = ""
        new_blueprint_data["tags"] = ""
        new_blueprint_data["description"] = ""
        new_blueprint_data["shortDescription"] = ""
        new_blueprint_data["externalLink"] = ""
        new_blueprint_data["entitledUsers"] = ""
        new_blueprint_data["entitledUserGroups"] = ""

        with open(blueprint_dir+"/"+file) as json_file:
            blueprint_build = json.load(json_file)
            for key, value in new_blueprint_data.items():
                if value == "":
                    for search_key, search_value in blueprint_build.items():
                        if search_key == key:
                            search_key = search_key.encode("utf-8")
                            if isinstance(search_value, list):
                                a = 0
                            elif isinstance(search_value, type(None)):
                                a = 0
                            else:
                                search_value = search_value.encode("utf-8")
                            new_blueprint_data[key] = search_value
        print "Inserting Blueprint: " + new_blueprint_data["name"]
        body = json.dumps(new_blueprint_data)
        headers = {'Content-Type': 'application/json'}
        req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
        if not parse_response(req.text):
            print "Error Inserting Blueprint: " + new_blueprint_data["name"]

def setup_email(url, username, password, email_params):
    print "Setting Email Server"
    if url.endswith('/'):
        request_url = url + 'api/emailconfig'
    else:
        request_url = url + '/api/emailconfig'
    
    new_email_data = collections.OrderedDict()

    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    if req.text:
        json_response = req.json()
        new_email_data["id"] = json_response["results"]["id"]
    
    new_email_data["mailHost"] = email_params["mail_host"]
    new_email_data["mailPort"] = email_params["mail_port"]
    new_email_data["mailPassword"] = email_params["mail_password"]
    new_email_data["mailUserName"] = email_params["mail_username"]
    new_email_data["mailFrom"] = email_params["mail_from"]
    new_email_data["mailBcc"] = email_params["mail_bcc"]
    new_email_data["mailFailureTo"] = email_params["mail_failto"]
    new_email_data["secureSmtpConnection"] = email_params["mail_securesmtp"]
    
    body = json.dumps(new_email_data)
    headers = {'Content-Type': 'application/json'}

    if url.endswith('/'):
        request_url = url + 'api/emailconfig/save'
    else:
        request_url = url + '/api/emailconfig/save'

    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if not parse_response(req.text):
            print  "Error Setting Email Server"

def setup_system(url, username, password, system_params):
    print "Setting Server Settings"
    if url.endswith('/'):
        request_url = url + 'api/appconfig/?setting_id='
    else:
        request_url = url + '/api/appconfig/?setting_id='

    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    if req.text:
        json_response = req.json()

        body = json_response["results"]
        for value in body:
            if value["key"] == "dchq.agent.connect.ip":
                value["value"] = system_params["system_url"]
            if value["key"] == "dchq.agent.connect.port":
                value["value"] = system_params["system_rmqport"]
            if value["key"] == "dchq.base.url":
                value["value"] = "https://" + system_params["system_url"]
            if value["key"] == "dchq.agent.script.url":
                value["value"] = "https://" + system_params["system_repo"] + "/repo/" + system_params["system_repo_version"] + "/agents/hcp_linux_agent.sh"
            if value["key"] == "dchq.title":
                value["value"] = system_params["system_title"]
            if value["key"] == "dchq.win.agent.script.url":
                value["value"] = "https://" + system_params["system_repo"] + "/repo/" + system_params["system_repo_version"] + "/agents/hcp_agent_install_windows.ps1"
            if value["key"] == "dchq.proxy.script.url":
                value["value"] = "https://" + system_params["system_repo"] + "/repo/" + system_params["system_repo_version"] + "/haproxy/HyperVProxy_Install_Windows_v1.3.ps1"

        body = json.dumps(body)

        headers = {'Content-Type': 'application/json'}
        if url.endswith('/'):
            request_url = url + 'api/appconfig/save-all?setting_id='
        else:
            request_url = url + '/api/appconfig/save-all?setting_id='

        req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
        if not parse_response(req.text):
            print "Error Setting Server Settings"

def setup_tenant(url, username, password, tenant_params):
    print "Setup Tenant"
    if url.endswith('/'):
        request_url = url + 'api/tenants'
    else:
        request_url = url + '/api/tenants'
    
    new_tenant_data = collections.OrderedDict()
    new_tenant_data["contactName"] = tenant_params["tenant_contactname"]
    new_tenant_data["userName"] = tenant_params["tenant_username"]
    new_tenant_data["name"] = tenant_params["tenant_name"]
    new_tenant_data["contactEmail"] = tenant_params["tenant_email"]
    new_tenant_data["email"] = tenant_params["tenant_email"]
    new_tenant_data["contactPhone"] = tenant_params["tenant_phone"]
    new_tenant_data["password"] = tenant_params["tenant_password"]
    
    if new_tenant_data["password"] == "":
        new_tenant_data["password"] = random_passwordgenerator()
        print "Using randomly generated password: " + new_tenant_data["password"]

    print "Create User for: " + new_tenant_data["email"]
    body = json.dumps(new_tenant_data)
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url,  data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    if not parse_response(req.text):
        print "Error Create User for: " + new_tenant_data["email"]

    response_json = json.loads(req.text)
    tenant_json = response_json["results"]
   
    #get registry accounts
    print "Assigning AZ and Resource Pool for tenant: " + new_tenant_data["email"] 
    for quota in tenant_params["quotas"]:
        if url.endswith('/'):
            request_url = url + 'api/registryaccounts/'
        else:
            request_url = url + '/api/registryaccounts/'
        req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        parsed_json = json.loads(response)
        results = parsed_json['results']
        for value in results:
            if value["name"] == quota["quota_provider"]:
                # got the provider
                # get AZ
                if url.endswith('/'):
                    request_url = url + 'api/registryaccounts/azs-all/'
                else:
                    request_url = url + '/api/registryaccounts/azs-all/'
                
                request_url = request_url + value["id"]
                req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
                response = req.text
                azs_json = json.loads(response)

                for az in azs_json['results']:
                    if az["name"] == quota['quota_az']:
                        print "Found AZ: " + az["name"]
                        print "Generating Quota: " + quota["quota_name"] + " with AZ: " + az["name"]
                        # create Quota and RP with AZ
                        if url.endswith('/'):
                            request_url = url + 'api/resourcepools'
                        else:
                            request_url = url + '/api/resourcepools'
        
                        new_quota_data = collections.OrderedDict()
                        new_quota_data["inactive"] = False
                        new_quota_data["rpType"] = "QUOTA"
                        new_quota_data["entitlementType"] = "TENANTS"
                        new_quota_data["entitledTenants"] = [ tenant_json ]
                        new_quota_data["quotaType"] = quota["qouta_type"] # valid quota type is open | restricted
                        new_quota_data["name"] = "QT." + value["name"].split(".")[0]  + "." + az["name"] + "." + quota["quota_name"]
                        new_quota_data["spendLimit"] = quota["quota_spendLimit"]
                        new_quota_data["cpu"] = quota["quota_cpu"]
                        new_quota_data["mem"] = quota["quota_mem"]
                        new_quota_data["disk"] = quota["quota_disk"]
                        new_quota_data["azId"] = az["id"]
                        new_quota_data["azName"] = az["name"]
                        body = json.dumps(new_quota_data)
                        headers = {'Content-Type': 'application/json'}
                        req = requests.post(request_url,  data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
                        if not parse_response(req.text):
                            print "Error Assigning AZ to: " + new_tenant_data["email"]
                            
                        quota_json = json.loads(req.text)

                        for rp in quota["rps"]:
                            print "Generating Resource Pool: " + rp["rp_name"] + " under Quota: " + quota["quota_name"] + " and user: " + new_tenant_data["email"]
                            new_rp_data = collections.OrderedDict()
                            new_rp_data["inactive"] = False
                            new_rp_data["rpType"] = "RESOURCE_POOL"
                            new_rp_data["entitlementType"] = "OWNER"
                            new_rp_data["entitledTenants"] = []
                            new_rp_data["entitledUserGroups"] = []
                            new_rp_data["entitledUsers"] = []
                            new_rp_data["quotaType"] = "restricted"
                            new_rp_data["resourcePoolTrigger"] = []
                            new_rp_data["prefix"] = "RP." + value["name"].split(".")[0]  + "." + az["name"] + "."
                            new_rp_data["name"] = "RP." + value["name"].split(".")[0]  + "." + az["name"] + "." + rp["rp_name"]
                            new_rp_data["spendLimit"] = rp["rp_spendLimit"]
                            new_rp_data["cpu"] = rp["rp_cpu"]
                            new_rp_data["mem"] = rp["rp_mem"]
                            new_rp_data["disk"] = rp["rp_disk"]
                            new_rp_data["azId"] = quota_json["results"]["id"] # in this case azId is the Quotaid
                        
                            body = json.dumps(new_rp_data)

                            req = requests.post(request_url,  data=body, headers=headers, auth=HTTPBasicAuth(new_tenant_data["email"], new_tenant_data["password"]), verify=False)

                            if not parse_response(req.text):
                                print "Error Assigning Resource Pool to: " + new_tenant_data["email"]
                        break
                
                # get non-entitled VPC
                
                if url.endswith('/'):
                    request_url = url + 'api/vpc/non-entitled/tenant/'
                else:
                    request_url = url + '/api/vpc/non-entitled/tenant/'
                
                request_url = request_url + tenant_json["id"] + '/'
                request_url = request_url + 'provider/' + value["accountType"] + '/' + value["id"]
                req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
                response = req.text
                vpcs_json = json.loads(response)

                for vpc in vpcs_json['results']:
                    if vpc["name"] == quota['quota_vpc']:
                        print "Found VPC: " + vpc["name"]
                        print "Assigning VPC: " + quota['quota_vpc'] + " to tenant: " + new_tenant_data["email"]
                        if url.endswith('/'):
                            request_url = url + 'api/vpc/'
                        else:
                            request_url = url + '/api/vpc/'
                        request_url = request_url + vpc["id"]
                        vpc["entitledTenants"] = [ tenant_json ]
                        vpc["entitlementType"] = "TENANTS"
                        body = json.dumps(vpc)
                        headers = {'Content-Type': 'application/json'}
                        req = requests.put(request_url,  data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
                        if not parse_response(req.text):
                            print "Error Assigning VPC to: " + new_tenant_data["email"]
                        break
                break
            

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) == 4:
        sys.exit("You need to provide an argument.  Usage: hypercloud_setup.py HCP_URL_or_IP username password [.] [reset_blueprints] [reset_tenants] [reset_providers] [reset_all] ")
    elif len(sys.argv) == 1:
        sys.exit("Usage: hypercloud_setup.py HCP_URL_or_IP username password [.] [reset_blueprints] [reset_tenants] [reset_providers] [reset_all] ")
    elif len(sys.argv) > 5:
        sys.exit("You provided too many arguments.  Usage: hypercloud_setup.py HCP_URL_or_IP username password [.] [reset_blueprints] [reset_tenants] [reset_providers] [reset_all]")

    HCP_URL = sys.argv[1]
    HCP_username = sys.argv[2]
    HCP_password = sys.argv[3]

    if sys.argv[4] == "reset_blueprints":
        print "reset_blueprints"
        reset_blueprints(HCP_URL, HCP_username, HCP_password)
    elif sys.argv[4] == "reset_plugins":
        print "reset_plugins"
        reset_plugins(HCP_URL, HCP_username, HCP_password)
    elif sys.argv[4] == "reset_tenants":
        print "reset_tenants"
        reset_tenants(HCP_URL, HCP_username, HCP_password)
    elif sys.argv[4] == "reset_providers":
        print "reset_providers"
        reset_all_providers(HCP_URL, HCP_username, HCP_password)
    elif sys.argv[4] == "reset_all":
        print "reset_all"
        reset_all_providers(HCP_URL, HCP_username, HCP_password)
        reset_blueprints(HCP_URL, HCP_username, HCP_password)
        reset_plugins(HCP_URL, HCP_username, HCP_password)
        reset_tenants(HCP_URL, HCP_username, HCP_password)
    else:
        if os.path.exists("setup.json") == False:
            print "setup file doesn't exist"
        else:
            with open('setup.json') as json_data:
                d = json.load(json_data)
            
            if d['setup_aws']:
                for value in d['aws_params']:
                    setup_aws(HCP_URL, HCP_username, HCP_password,value['name'], value['username'], value['password'], value['groupName'])

            if d['setup_gcp']:
                for value in d['gcp_params']:
                    setup_gcp(HCP_URL, HCP_username, HCP_password,value['name'], value['username'], value['password'], value['groupName'])
            
            if d['setup_azure']:
                for value in d['azure_params']:
                    setup_azure(HCP_URL, HCP_username, HCP_password,value['name'], value['email'], value['url'], value['username'], value['password'], value['groupName'])

            if d['setup_blueprints']:
                if os.path.exists(os.path.join(".", "blueprints")):
                    shutil.rmtree(os.path.join(".", "blueprints"))
                blueprint_dir = os.path.join(".", "blueprints")
                os.mkdir(blueprint_dir)

                for value in d['blueprints']:
                    req = requests.get(value)
                    json_response = req.json()
                    filename = os.path.join(blueprint_dir, json_response['id'] + ".json")
                    with open(filename, "w") as f: 
                        f.write(req.text) 
                setup_blueprints(HCP_URL, HCP_username, HCP_password, blueprint_dir)

            if d['setup_plugins']:
                if os.path.exists(os.path.join(".", "plugins")):
                    shutil.rmtree(os.path.join(".", "plugins"))
                plugin_dir = os.path.join(".", "plugins")
                os.mkdir(plugin_dir)

                for value in d['plugins']:
                    req = requests.get(value)
                    json_response = req.json()
                    filename = os.path.join(plugin_dir, json_response['referenceId'] + ".json")
                    with open(filename, "w") as f: 
                        f.write(req.text) 
                setup_plugins(HCP_URL, HCP_username, HCP_password, plugin_dir)
            
            if d['setup_email']:
                setup_email(HCP_URL, HCP_username, HCP_password, d['email_params'])

            if d['setup_system']:
                setup_system(HCP_URL, HCP_username, HCP_password, d['system_params'])
            
            if d['setup_tenant']:
                for value in d['tenant_params']:
                    setup_tenant(HCP_URL, HCP_username, HCP_password, value)




