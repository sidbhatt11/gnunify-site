from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'GNUnify'
settings.subtitle = 'Feb 13,14'
settings.author = 'Siddharth Bhatt'
settings.author_email = 'sidbhatt11@yahoo.in'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '86b17a4f-628a-4780-b7e9-4cd146e19648'

settings.email_server = 'smtp.gmail.com:587'
settings.email_sender = 'yourid@gmail.com'
settings.email_login = 'yourid@gmail.com:yourgmailpassword'

settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
