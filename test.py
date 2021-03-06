import json
import logging
import os
import requests
import sys
import adal

def turn_on_logging():
    logging.basicConfig(level=logging.DEBUG)
    #or,
    #handler = logging.StreamHandler()
    #adal.set_logging_options({
    #    'level': 'DEBUG',
    #    'handler': handler
    #})
    #handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))

# You can provide account information by using a JSON file. Either
# through a command line argument, 'python sample.py parameters.json', or
# specifying in an environment variable of ADAL_SAMPLE_PARAMETERS_FILE.
#
# The information inside such file can be obtained via app registration.
# See https://github.com/AzureAD/azure-activedirectory-library-for-python/wiki/Register-your-application-with-Azure-Active-Directory
#
# {
#    "resource": "YOUR_RESOURCE",
#    "tenant" : "YOUR_SUB_DOMAIN.onmicrosoft.com",
#    "authorityHostUrl" : "https://login.microsoftonline.com",
#    "clientId" : "YOUR_CLIENTID",
#    "clientSecret" : "YOUR_CLIENTSECRET"
# }


parameters_file = (sys.argv[1] if len(sys.argv) == 2 else
                   os.environ.get('ADAL_SAMPLE_PARAMETERS_FILE'))

if parameters_file:
    with open(parameters_file, 'r') as f:
        parameters = f.read()
    sample_parameters = json.loads(parameters)
else:
    raise ValueError('Please provide parameter file with account information.')

authority_url = (sample_parameters['authorityHostUrl'] + '/' +
                 sample_parameters['tenant'])
GRAPH_RESOURCE = '00000002-0000-0000-c000-000000000000'
RESOURCE = sample_parameters.get('resource', GRAPH_RESOURCE)

#uncomment for verbose log
turn_on_logging()

### Main logic begins
context = adal.AuthenticationContext(
    authority_url, validate_authority=sample_parameters['tenant'] != 'adfs',
    )

token = context.acquire_token_with_client_credentials(
    RESOURCE,
    sample_parameters['clientId'],
    sample_parameters['clientSecret'])
### Main logic ends

print('Here is the token:')
print(json.dumps(token, indent=2))

access_token = token["accessToken"]
vendors_url = sample_parameters.get("baseUrl").replace("{{tenant_id}}", sample_parameters["tenant"])
results = requests.get(
    vendors_url,
    headers={'Authorization': 'Bearer ' + access_token},
)

print(vars(results))
