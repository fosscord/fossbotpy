import filetype

from ..requestsender import Wrapper

from ..logger import LogLevel, Logger

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

class Fileparse(object):
	__slots__ = ['log', 'edited_s']
	def __init__(self, s, log): #s is the requests session object
		self.log = log
		self.edited_s = Wrapper.edited_req_session(s, {"remove": ["Authorization", "X-Fingerprint", "X-Super-Properties"]})
		
	def parse(self, filelocation, isurl): #returns mimetype and extension if detected
		fd = b""
		if isurl:
			result = urlparse(filelocation)
			if all([result.scheme, result.netloc]): #if a link...
				fd = Wrapper.send_request(self.edited_s, 'get', filelocation, log=self.log).content
				kind = filetype.guess(fd)
				if kind is None:
					Logger.log('Unsupported file type. Will attempt to send anyways.', LogLevel.WARNING, self.log)
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				Logger.log('Invalid link.', LogLevel.WARNING, self.log)
				return 'invalid', 'invalid', fd
		else:
			try:
				kind = filetype.guess(filelocation)
				if kind is None:
					Logger.log('Unsupported file type. Will attempt to send anyways.', LogLevel.WARNING, self.log)
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			except Exception as e:
				Logger.log(repr(e), LogLevel.WARNING, self.log)
				return 'invalid', 'invalid', fd
