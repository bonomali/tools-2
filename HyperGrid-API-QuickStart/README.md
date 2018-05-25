
![logo](https://i.imgur.com/l7qycqV.jpg "logo")
# HyperGrid REST API Quick Start Guide
## For HyperCloud Portal
### Simple Steps to Begin using the REST API in Minutes


John Masci – jmasci@hypergrid.com 


This document provides a quick start guide for implementing the HyperGrid API. 

It will allow users to begin interfacing with the HyperCloud API for automation, practical scripting, and reporting within hours and not days. 

In addition to providing foundational background it includes practical samples, and simple cut & paste command line examples to enable users to quickly interface with the API. 

This document will cover:

* Authentication with the APIs
* Provisioning applications and VMs through the API
* Fetching data in a clean and easily manageable format
    o Searching through results to collect & return individual values 

Some simple cross-platform tools are used to begin interfacing with the HyperCloud’s API:

* **cURL** – a command line tool available for OS X, Linux, and Windows to send & receive HTTP requests to/from the HyperCloud Platform 
* **JQ** – command line tool used to cleanly & quickly filter data retrieved from the API as JSON objects into plain text

To follow along using Ubuntu Linux, the tools can be installed quickly by running the following commands:

* `sudo apt install curl`
* `sudo apt install jq`

Check if installations were successful by running the following commands to output the versions:

* `jq --version`
* `curl -v`

### Following document is used for the API reference:

HyperCloud Portal API – Application & VM Oriented: https://goo.gl/IqQ6Ln

# Getting Started

The first step is to address authentication. There are two interfaces you can interact with, one primarily for managing infrastructure, HyperVue Manager, and one for managing applications & VMs, HyperCloud Portal. They both can be interfaced similarly with their own API’s, but authentication varies slightly. This document will cover the HyperCloud Portal.

# HyperCloud Portal: Authentication

Interfacing with HyperCloud Manager will require: 

* IP Address of the HyperCloud Portal (VM)
* Username & Password
* Access key & Secret Key

The system uses basic auth for authentication which uses a generated access key & secret key to authorize commands. After logging in, create the two keys by clicking the menu in the top right corner of the portal & select ‘Access Key’ from the drop down menu. 

![step one](https://i.imgur.com/laZ1G1D.png)


![step two](https://i.imgur.com/KDkLOjh.png)


The third step, record both the Access Key & the Secret Key for future authentication.

Basic Auth will use the Access Key and Secret Key. The syntax for a curl command is: 

`curl --user accesskey:secretkey https://<HyperCloud Portal IP>/REST_End_Point`

example:


`JMasci@Grid-JMasci-MBP:~$ curl --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfgzDTcvz3su https://hypercloud.skygrid.cloud/api/1.0/blueprints`


# Collecting Data with the REST API 

Continuing from the above authentication example, we use the /blueprints endpoint to capture the names & descriptions of the existing application Blueprints used for app provisioning. 

Syntax:

`curl --user accesskey:secretkey https://<HyperCloud Portal IP>/REST_End_Point`

cURL Options which may be helpful:

* ‘-s’ option is used to silence the transmission information from the output
* ‘-k’ option can be used during testing to allow for insecure transmissions, if an SSL certificate is not yet enabled

This example will output the entire JSON object. A truncated output would be returned as follows:

```sh
Masci@Grid-JMasci-MBP:~$ curl –s --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints

{"errors":false,"messages":[],"requestId":null,"results":[{"id":"2c9180875cd63fe5015cec1f86196a48","lastModifiedBy":"kelly murphy","created":1498610107929,"lastUpdated":1499347336373,"createdBy":"admin","dynamicAttributes":{},"inactive":false,"deleted":false,"tenantPk":"402881834d9ee4d1014d9ee5d73f0010","entitlementType":"CUSTOM","entitledUserGroups":null,"entitledUsers":null,"entitledUsersPks":[],"entitledGroupsPks":["2c9180865bb5819e015bda39e2df6603","2c9180865ba6d741015bac263cf40737","2c9180865bb5819e015bda39bb106600"],"ownerId":null,"composeVersion":"VM","name":"Azure Ubuntu 4GB","version":"1.0","uuid":null,"reason":null,"tags":null,"description":"Ubuntu 14.04 with 1 vCPU and 3.5 GB of Memory","yml":null,"leaseTime":null,"userName":"402881834d9ee4d1014d9ee5d73f0014","shortDescription":null,"externalLink":null,"imageLink":"/src/icon/library/VM_COMPOSE/OPERATING_SYSTEM/ubuntu.png","appTaskProcessingTime":null,"totalStars":1,"totalRun":6,"editable":null,"userStarred":null,"gist":null,"image":null,"images":[],"serviceTypes":[],"blueprintType":"VM_COMPOSE","datacenter":null,"visibility":"READABLE","customizationsText":null,"customizationsMap":null,"params":[],"gridBlueprintId":null,"entitlementTypeProvision":null,"entitledUserGroupsProvision":[],"entitledUsersProvision":[],"licenseModel":null,"costPolicyExist":"$ 54.0","cloudProvider":null},{"id":"2c9180875cd63fe5015cec0e7ffe68c7","lastModifiedBy":"kelly murphy","created":1499790099341,"lastUpdated":1499790099341,"createdBy":"admin","dynamicAttributes":{},

...
```


The JSON output can be made easier to read and work with by piping the outputs through JQ. This response is a JSON output where JQ is used to clean up the response and make it easier to read, or allow for isolating values which can be used in scripts.

Pipe the output of the original command to ‘JQ’ by appending it with ‘| jq’. JQ will now process the JSON content delivered by the request. 

### Example:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq

{
  "errors": false,
  "messages": [],
  "requestId": null,
  "results": [
    {
      "ownerId": null,
      "composeVersion": "VM",
      "name": "Azure Ubuntu 4GB",
      "version": "1.0",
      "uuid": null,
      "reason": null,
      "tags": null,
      "description": "Ubuntu 14.04 with 1 vCPU and 3.5 GB of Memory",
      "yml": null,
      "leaseTime": null,
      "userName": "402881834d9ee4d1014d9ee5d73f0014",
      "shortDescription": null,
      "externalLink": null,
      "imageLink": "/src/icon/library/VM_COMPOSE/OPERATING_SYSTEM/ubuntu.png",
      "appTaskProcessingTime": null,
      "totalStars": 1,
      "totalRun": 6,
      "editable": null,
      "userStarred": null,
      "gist": null,
      "image": null,
      "images": [],
      "serviceTypes": [],
      "blueprintType": "VM_COMPOSE",
      "datacenter": null,
      "visibility": "READABLE",
      "customizationsText": null,
      "customizationsMap": null,
      "params": [],
      "gridBlueprintId": null,
      "entitlementTypeProvision": null,
      "entitledUserGroupsProvision": [],
      "entitledUsersProvision": [],
      "licenseModel": null,
      "costPolicyExist": "$ 54.0",
      "cloudProvider": null
    }
}
```

Individual elements of the JSON output can be selected with JQ as well. This example shows capturing a list of names for each Blueprint within the HyperCloud environment:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq '.results[].name'

"Azure Ubuntu 4GB"
"Puppet Module for Tomcat (Ubuntu)"
"Nginx"
"3-Tier Java (Nginx – Tomcat – MySQL)"
```



This example shows capturing both the name & description of each Blueprint in the HyperCloud environment for this user:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user xrw4yHWMTz2JY0:nUxmjXC295HHlWMTfjhgzDT5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq '.results[] | { name, description }'

{
  "name": "Azure Ubuntu 4GB",
  "description": "Ubuntu 14.04 with 1 vCPU and 3.5 GB of Memory"
}
{
  "name": "Puppet Module for Tomcat (Ubuntu)",
  "description": "A single Ubuntu VM that automates the installation of Tomcat using a Puppet module"
}
{
  "name": "Nginx",
  "description": "Opensource loadbalancer"
}
{
  "name": "3-Tier Java (Nginx – Tomcat – MySQL)",
  "description": "3 tier"
}
```

# Searching JSON Outputs for Values

In the instance of creating custom reports or writing scripts, it may be necessary to search for elements within the HyperCloud environment. To report all the configuration details of an individual Blueprint, JQ can be instructed to output the values of Blueprint which match a specific name. 

In this example, a command is issued to output the details of a Blueprint named ‘Azure Ubuntu 4GB’:


```sh
Masci@Grid-JMasci-MBP:~$ curl -s --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq '.results[] | select(.name=="Azure Ubuntu 4GB")'

{
  "ownerId": null,
  "composeVersion": "VM",
  "name": "Azure Ubuntu 4GB",
  "version": "1.0",
  "uuid": null,
  "reason": null,
  "tags": null,
  "description": "Ubuntu 14.04 with 1 vCPU and 3.5 GB of Memory",
  "yml": null,
  "leaseTime": null,
  "userName": "402881834d9ee4d1014d9ee5d73f0014",
  "shortDescription": null,
  "externalLink": null,
  "imageLink": "/src/icon/library/VM_COMPOSE/OPERATING_SYSTEM/ubuntu.png",
  "appTaskProcessingTime": null,
  "totalStars": 1,
  "totalRun": 6,
  "editable": null,
  "userStarred": null,
  "gist": null,
  "image": null,
  "images": [],
  "serviceTypes": [],
  "blueprintType": "VM_COMPOSE",
  "datacenter": null,
  "visibility": "READABLE",
  "customizationsText": null,
  "customizationsMap": null,
  "params": [],
  "gridBlueprintId": null,
  "entitlementTypeProvision": null,
  "entitledUserGroupsProvision": [],
  "entitledUsersProvision": [],
  "licenseModel": null,
  "costPolicyExist": "$ 54.0",
  "cloudProvider": null
}
```


This command can be piped again to capture only specific elements of the JSON output for a Blueprint named ‘Azure Ubuntu 4GB’. In this example, the command will only return the name, description, and cost policy associated with the Blueprint:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq '.results[] | select(.name=="Azure Ubuntu 4GB") | { name, description, costPolicyExist }'

{
  "name": "Azure Ubuntu 4GB",
  "description": "Ubuntu 14.04 with 1 vCPU and 3.5 GB of Memory",
  "costPolicyExist": "$ 54.0"
}
```


It may be necessary to capture only a single raw value from the output. JQ also provides an option to retrieve this raw value, which can be passed to additional scripts or reports. 

Note the ‘-r’ option for JQ to remove the JSON formatting and quotations around the value.

```sh
JMasci@Grid-JMasci-MBP:~$ curl -ks --user xrdqR3jxWHjw4yHz2JY0:nUxmjXC295HHlWMTfjhgzDTcvzbIQxmTFyH5X3su https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq -r '.results[] | select(.name=="Azure Ubuntu 4GB") | .costPolicyExist'

$ 54.0
```


# Provisioning a VM Blueprint with a cURL Command 

‘Blueprints’ in the HyperCloud Portal Library serve as templates for application deployment. This allows users to provision VMs and full stack applications from scripts, the command line, automation platforms, or service request systems. Blueprint parameters allow users to customize the applications at the time of deployment as well. 

The two values will be needed to provision a VM blueprint:

* Blueprint ID
* Cloud Provider ID

The blueprint ID can be found in the UI or via the API. 

From the web UI:

![blueprint ID](https://i.imgur.com/xqf3Ixc.png)

From the API:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user cg8wqGN5chz3x14oUGti:ix9MLKDPPj1jAcv8a7dPptlPm9QFGEaB1CfU07uO https://hypercloud.skygrid.cloud/api/1.0/blueprints | jq -r '.results[] | select(.name=="Ubuntu 4GB") | .id'

2c9180865d30e6ad015d531051ad0572
```


The Cloud Provider ID can be found from the HyperCloud Portal web UI or the API.

From the web UI:

Select ‘Cloud Providers’ from the left navigation pane, clicking a desired Cloud Provider, and selecting ‘Edit’ from the right hand ‘Actions’ column.

The web UI URL will display the ID number, in this example 2c9180865b7ced4c015b7e50122b0002.

![cloud provider ID](https://i.imgur.com/15v1z9R.png)

From the API:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -s --user pdKLzCuJX1jb19KvrP20:b78Wxqw17TeljUembjCeNNCjfgBDCIxhp6xrHLYm https://hypercloud.skygrid.cloud/api/registryaccounts/manage | jq '.results[] | { name, accountType, id }'

{
  "name": "SkyGridC01 (HCS)",
  "accountType": "HYPER_GRID",
  "id": "2c9180865b7ced4c015b7e50122b0002"
}
{
  "name": "AWS",
  "accountType": "AWS_EC2",
  "id": "2c9180875cd63fe5015cec0363a5681a"
}
{
  "name": "Microsoft Azure",
  "accountType": "MICROSOFT_ARM",
  "id": "2c9180875cd63fe5015cec0490446829"
}
```


A POST API method is used to provision the Blueprint with the API. The configuration data is sent in JSON format through the API. The command will include the following options:

* Two headers:
* `-H "Accept: application/json"`
* `-H "Content-type: application/json"`
* `‘-X POST’ option to send the data`
* `‘-d {<data>}’ JSON formatted data`

The syntax is as follows:

```sh
curl -sk --user cg8wqGN5chz3x14oUGti:ix9MLKDPPj1jAcv8a7dPptlPm9QFGEaB1CfU07uO -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"blueprint":"2c9180865d30e6ad015d531051ad0572","cloudProvider":"2c9180865b7ced4c015b7e50122b0002","cluster":null,"params":[]}' "https://hypercloud.skygrid.cloud/api/dockerservers/sdi" | jq '.'
```

The command will also return JSON data which describes the blueprint being provisioned, including the dynamically assigned VM name.  This output is shown being piped through JQ to clean up the data. 

Here is a sample execution & output:

```sh
JMasci@Grid-JMasci-MBP:~$ curl -k --user cg8wqGN5chz3x14oUGti:ix9MLKDPPj1jAcv8a7dPptlPm9QFGEaB1CfU07uO -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"blueprint":"2c9180865d30e6ad015d531051ad0572","cloudProvider":"2c9180865b7ced4c015b7e50122b0002","cluster":null,"params":[]}' "https://hypercloud.skygrid.cloud/api/dockerservers/sdi" | jq '.'

{
  "errors": false,
  "messages": [],
  "requestId": null,
  "results": {
    "id": "2c9180865d30e6ad015d622df0e07278",
    "inactive": false,
    "deleted": false,
    "lockVersion": null,
    "lastModifiedDate": null,
    "lastModifiedBy": "john masci",
    "createdDate": null,
    "createdBy": "john masci",
    "owner": {
      "id": "2c9180865ba6d741015bb0bebaf50ecd",
      "inactive": null,
      "deleted": null,
      "username": null,
      "firstname": null,
      "lastname": null
    },
    "ownerPk": "2c9180865ba6d741015bb0bebaf50ecd",
    "tenant": {
      "id": "402881834d9ee4d1014d9ee5d73f0010",
      "inactive": null,
      "deleted": null,
      "name": null
    },
    "tenantPk": "402881834d9ee4d1014d9ee5d73f0010",
    "name": "ubuntu-gl6",
    "nodeName": "Ubuntu4G",
    
    
...
```

