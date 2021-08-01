# business_central-poc


- `pip install adal`
- follow instructions [here](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/automation-apis-using-s2s-authentication) to set up Azure AD and Business Central
- copy parameters.json.dist to parameters.json
- edit parameters.json and enter in application values from above
- run `python3 test.py parameters.json`
