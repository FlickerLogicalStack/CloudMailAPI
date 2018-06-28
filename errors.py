class MailCloudBaseException(Exception):
	pass

class MailCloudWrongAuthData(MailCloudBaseException):
	pass

class MailCloudUnexpectedTokenError(MailCloudBaseException):
	pass
