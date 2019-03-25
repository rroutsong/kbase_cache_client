class NoCacheIdentifiers(Exception):
    pass

class HTTPRequestError(Exception):
    pass

class UnknownRequestError(Exception):
    pass

class DownloadDirNotaDir(Exception):
    pass

class DownloadDirNotWriteable(Exception):
    pass

class CacheNonexistent(Exception):
    pass

class AuthorizationTokenNotSet(Exception):
    pass