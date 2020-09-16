import io
from googleapiclient.http import MediaIoBaseDownload
from drive_download import list_folder


def download(drive, folder_id):
    files = list_folder(folder_id=folder_id)
    for file in files:
        filename = file['name']
        file_id = file['id']
        request = drive.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

