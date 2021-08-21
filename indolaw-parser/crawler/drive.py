from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class DriveUploader:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def drive_upload(self, uu_name: str):
        file = self.drive.CreateFile({'title': uu_name})
        file.SetContentFile(uu_name + '.pdf')
        file.Upload(param={'convert': True})

        original_file = self.drive.CreateFile({'title': uu_name + '.pdf'})
        original_file.SetContentFile(uu_name + '.pdf')
        original_file.Upload()

        uploadedFile = self.drive.CreateFile({'id': file['id']})
        uploadedFile.GetContentFile(uu_name + '.txt', mimetype='text/plain')
