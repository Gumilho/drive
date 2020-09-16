from googleapiclient import discovery
from oauth2client import file, client, tools
from httplib2 import Http


def get_service():
    scopes = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('drive_write.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', scopes)
        creds = tools.run_flow(flow, store)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))
