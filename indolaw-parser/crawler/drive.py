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



# # Auto-iterate through all files that matches this query
# file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
# for file1 in file_list:
#     print('title: {}, id: {}'.format(file1['title'], file1['id']))

# # Paginate file lists by specifying number of max results
# for file_list in drive.ListFile({'maxResults': 10}):
#     print('Received {} files from Files.list()'.format(len(file_list))) # <= 10
#     for file1 in file_list:
#         print('title: {}, id: {}'.format(file1['title'], file1['id']))