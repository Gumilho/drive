import datetime
import pathlib
import json
import os
import io
from trello import TrelloClient
from trello.trellolist import List
from trello.card import Card
from trello.board import Board
from trello.label import Label
from Secret import api_key, api_secret, token
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
from pathlib import Path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("members.json", 'r', encoding="utf-8") as f:
    members = json.load(f)

with open("settings.json", 'r') as f:
    settings = json.load(f)

def get_service():
    scopes = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('drive_write.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', scopes)
        creds = tools.run_flow(flow, store)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))


def download(path, folder_id, service):
    q = f"'{folder_id}' in parents"
    files = list_folder(q, service)
    
    for file in files:
        filename = path / file['name']
        file_id = file['id']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))


def list_folder(q, service):
    return service.files().list( # pylint: disable=maybe-no-member
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        q=q,
        pageSize=1000).execute().get('files', []) 


def drive_search(project, role, chapter, service):
    path = f'{project},{role},{chapter}'
    folders = path.split(',')
    q = "'1FPnMkcY2uXxECMyQhHdsz1M7NgB7fiOs' in parents or '1At9XBjQaA0QM_NCFAvUHVJv6ozs6tVle' in parents"
    files = list_folder(q, service)
    for folder in folders:
        flag = False
        for file in files:
            try:
                chapter = float(file["name"])
                if chapter.is_integer():
                    file["name"] = str(int(chapter))
            except:
                pass

            if file['name'] == folder:
                file_id = file['id']
                flag = True
                break

        if not flag:
            print(path)
            print('------------erro------------')
            raise Exception("Chapter not found")
        q = f"'{file_id}' in parents"
        files = list_folder(q, service)
    return file_id


def cd(*path):
    for name in path:
        name = str(name)
        if not os.path.isdir(name):
            os.mkdir(name)
        os.chdir(name)


def find(iterable, name):
    return next((x for x in iterable if x.name == name), None)


def get_info(card):
    chapter = float(card.name.split(' ')[1])
    if chapter.is_integer():
        chapter = int(chapter)
    role = ' '.join(card.name.split()[:-1])
    return chapter, role


if __name__ == '__main__':
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
                "Bully": "When You're Targeted by the Bully",
                "Pond Snail Robber": "Pond Snail Robber"}

    role_dict = {"Cleaning": "1 - RAW",
                "Redraw": "2 - Falta Redraw",
                "Tradução": "",
                "RAW": "1 - RAW",
                "Type": "3 - 100% Clean",
                "Postar": "4 - Completo",
                }
    
    
    client = TrelloClient(api_key=api_key, api_secret=api_secret, token=token)
    board = find(client.list_boards(), 'Quadro Teste') # type: Board
    labels = board.get_labels()
    label_avail = find(labels, "Disponível") # type: Label
    label_unavail = find(labels, "Indisponível") # type: Label
    lists = board.list_lists() # type: list[List]
    for name, roles in members[settings["User"]].items():
        for tlist in lists:
            if tlist.name == name:
                for card in tlist.list_cards(): # type: Card
                    if card.labels[0] == label_avail:
                        chapter, role = get_info(card)
                        if role in roles:
                            project = name_dict[name]
                            role = role_dict[role]
                            if role:
                                path = Path(os.path.join(*[settings["Download Folder"], project, role, str(chapter)]))
                                print(path)
                                if not os.path.exists(path):
                                    try:
                                        folder_id = drive_search(project, role, chapter, service=service)
                                    except Exception:
                                        print("cant search")
                                        continue

                                    path.mkdir(parents=True, exist_ok=True)
                                    download(path, folder_id, service)


                        

