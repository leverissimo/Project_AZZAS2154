from google.oauth2 import service_account

def getCredentials(serviceAccountPath:str) -> service_account:



    return service_account.Credentials.from_service_account_file(serviceAccountPath)
