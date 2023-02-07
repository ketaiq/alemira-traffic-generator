class UserAPIEndPoint:
    URI = "https://userapi.alms.crab.alemira.com/api/v1/"
    FILE_URI = "https://alms.crab.alemira.com/fileapi/api/v1/"
    TIMEOUT_MAX = 180

    def __init__(self, client):
        self.uri = self.URI
        self.file_uri = self.FILE_URI
        self.client = client
