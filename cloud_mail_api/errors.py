class CloudMailBaseException(Exception):
	pass

class CloudMailWrongAuthData(CloudMailBaseException):
	pass

class CloudMailUnexpectedTokenError(CloudMailBaseException):
	pass
