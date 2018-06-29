class CloudMailBaseException(Exception):
	pass

class CloudMailWrongAuthData(CloudMailBaseException):
	pass

class CloudMailUnexpectedTokenError(CloudMailBaseException):
	pass

class CloudMailRequireLoginError(CloudMailBaseException):
	pass

class CloudMailSdcGettingError(CloudMailBaseException):
	pass
