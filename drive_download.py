import io
from oauth2 import get_service
from download import download
SCAN_ID = "1FPnMkcY2uXxECMyQhHdsz1M7NgB7fiOs"
service = get_service()

name_dict = {"Angel": "Angel",
             "Servant": "First Class Servant",
             "Homura": "Homura sensei wa Tabun Motenai",
             "Omotenashi": "Isekai Omotenashi Gohan",
             "King's Concubine": "King's Concubine",
             "Kobayashi Kanna": "Kobayashi-san Chi no Maid Dragon - Kanna no Nichijou",
             "Sayonara": "Sayonara Rose Garden",
             "Second Lead Complex": "Second Lead Complex",
             "Abandoned Empress": "The Abandoned Empress",
             "The Garden of Red Flowers": "The Garden of Red Flowers",
             "Hourglass": "The Villainess Reverses the Hourglass",
             "Wataten": "Watashi ni Tenshi ga Maiorita",
             "Bully": "When You're Targeted by the Bully"}

role_dict = {"Cleaning": 'a',
             "Redraw": "First Class Servant",
             "Tradução": "Homura sensei wa Tabun Motenai",
             "RAW": "Isekai Omotenashi Gohan",
             "Type": "King's Concubine"}
file_id = drive_search(name_dict[list_name], "1 - RAW", 30)
download(service, file_id)

def list_folder(folder_id):
    q = f"'{folder_id}' in parents"
    return service.files().list(
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q=q,
        pageSize=1000).execute().get('files', []),

def drive_search(project, role, chapter):
    path = f'{project},{role},cap {str(chapter)}'
    folders = path.split(',')
    # download_id = []
    # first search
    file_id = SCAN_ID
    for folder in folders:
        files = list_folder(file_id)
        flag = False
        for file in files:
            if file['name'].lower().startswith('cap'):
                chapter = int(file['name'].split(' ')[1])
                file['name'] = "cap " + str(chapter)
            if file['name'] == folder:
                file_id = file['id']
                flag = True
        if not flag:
            print('------------erro------------')
    return file_id


file_id = drive_search("The Abandoned Empress", "1 - RAW", 30)
download_drive(service, file_id)
