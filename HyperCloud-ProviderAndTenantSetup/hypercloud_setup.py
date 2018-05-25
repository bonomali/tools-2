
import requests
from requests.auth import HTTPBasicAuth
# import pprint
import json
import sys
import os
import collections
import shutil
import pprint

def reset_blueprints(URL, username, password):
    if URL.endswith('/'):
        request_url = URL + 'api/blueprints/'
    else:
        request_url = URL + '/api/blueprints/'

    print request_url
    print username
    print password

    req = requests.get(request_url + 'filter?page=0&pageSize=10000&q=MY', auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        delete_url = request_url + value['id']
        print "Deleting BluePrint: " + delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        print response

def reset_plugins(URL, username, password):
    if URL.endswith('/'):
        request_url = URL + 'api/plugins/'
    else:
        request_url = URL + '/api/plugins/'

    print request_url
    print username
    print password

    req = requests.get(request_url + 'manage?page=0&pageSize=10000', auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        delete_url = request_url + value['id']
        print "Deleting Plugins: " + delete_url
        req = requests.delete(delete_url, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        print response

def reset_tenants(URL, username, password):
    if URL.endswith('/'):
        request_url = URL + 'api/tenants/'
    else:
        request_url = URL + '/api/tenants/'
    req = requests.get(request_url, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text

    parsed_json = json.loads(response)
    results = parsed_json['results']
    for value in results:
        reset_tenant(URL, username, password, value['email'])
        delete_url = request_url + value['id']
        print "Deleting Tenant..."
        print delete_url
        # req = requests.delete(request_url, auth=HTTPBasicAuth(username, password), verify=False)
        # response = req.text

def reset_tenant(URL, username, password, email_id):
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
            print request_url
            # response = requests.post(request_url, auth=HTTPBasicAuth(username, password), verify=False, data=body)
            reset_tenant_containers(URL, tenant_user_id, tenant_password)
            # reset_tenant_clusters(URL, tenant_user_id, tenant_password)
            # reset_tenant_vms(URL, tenant_user_id, tenant_password)
            # reset_tenant_resourcepools(URL, tenant_user_id, tenant_password)

def reset_tenant_containers(URL, username, password):
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
        body = json.dumps(results)
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


def reset_onprem_providers(URL, username, password):
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
    new_provider_data["accountType"] = "AWS_EC2"
    body = json.dumps(new_provider_data)
    print request_url
    print username
    print password
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text
    print response

def setup_gcp(url, username, password, gcp_accountname, gcp_email, gcp_json, gcp_groupname):
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
    new_provider_data["accountType"] = "GOOGLE_COMPUTE_ENGINE"
    body = json.dumps(new_provider_data)
    print request_url
    print username
    print password
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text
    print response

def setup_azure(url, username, password, azure_accountname, azure_email, azure_region, azure_username, azure_password, azure_groupname):
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
    new_provider_data["name"] = azure_accountname
    new_provider_data["email"] = azure_email
    new_provider_data["region"] = azure_region
    new_provider_data["accountType"] = "MICROSOFT_ARM"
    body = json.dumps(new_provider_data)
    print request_url
    print username
    print password
    headers = {'Content-Type': 'application/json'}
    req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
    response = req.text
    print response

def setup_blueprints(url, username, password, blueprint_dir):
  
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
        new_blueprint_data["entitlementType"] = ""
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

        body = json.dumps(new_blueprint_data)
        print body
        print request_url
        print username
        print password
        headers = {'Content-Type': 'application/json'}
        req = requests.post(request_url, data=body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
        response = req.text
        print response
            # print blueprint_build['id']
    # new_build = build_file.readlines()


if __name__ == "__main__":

    # Pull latest announcements from AWS
    #     req = requests.get('https://aws.amazon.com/new/')
    # req.status_code
    # response = req.text
    #
    #         # Add to Firebase announcements
    #         url = 'https://intense-heat-6839.firebaseio.com/announcements/aws.json'
    #         body = json.dumps(announcement)
    #         response = requests.post(url, data=body)

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
#    elif sys.argv[4] == "reset_onprem_providers":
#        print "reset_onprem_providers"
#        reset_onprem_providers(HCP_URL, HCP_username, HCP_password)
#    elif sys.argv[4] == "reset_public_providers":
#        print "reset_public_providers"
#        reset_public_providers(HCP_URL, HCP_username, HCP_password)
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
        # config_file = open(sys.argv[4], 'r')
        if os.path.exists("setup.json") == False:
            print "setup file doesn't exist"
        else:
            with open('setup.json') as json_data:
                d = json.load(json_data)
            if d['setup_aws']:
                setup_aws(HCP_URL, HCP_username, HCP_password,d['aws_params']['name'], d['aws_params']['username'], d['aws_params']['password'], d['aws_params']['groupName'])

            if d['setup_gcp']:
                setup_gcp(HCP_URL, HCP_username, HCP_password,d['gcp_params']['name'], d['gcp_params']['username'], d['gcp_params']['password'], d['gcp_params']['groupName'])
            
            if d['setup_azure']:
                setup_azure(HCP_URL, HCP_username, HCP_password,d['azure_params']['name'], d['azure_params']['email'], d['azure_params']['region'], d['azure_params']['username'], d['azure_params']['password'], d['azure_params']['groupName'])

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
                #setup_blueprints(HCP_URL, HCP_username, HCP_password, blueprint_dir)
        #    pprint.pprint(d)
        # setup_new_env(HCP_URL, HCP_username, HCP_password, os.path.join(".", "blueprints"))
        # blueprint_dir = sys.argv[4]
        #setup_new_env(HCP_URL, HCP_username, HCP_password, blueprint_dir)




