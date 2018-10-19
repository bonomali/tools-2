Python Script to setup HCP.

Usage:
To setup HCP, call the script with these following parameters:
python hypercloud_setup.py https://<HCP_URL> <HCP_Username> <HCP_Password> .

the '.' at the back determines that it will setup HCP using the setup.json

setup.json file is the descriptor file that will be used to drive the parameter of the setup.

setup.json quick guide:
- setting setup_* to true will execute the functions to setup the appropriate settings
- aws_params, gcp_params, azure_params, and tenant_params are arrays. Meaning that more than 1 provider information can be setup. However, the name has to be unique among HCP.
- setting up tenant requires knowing the names of the VPC and AZ to be used upfront
