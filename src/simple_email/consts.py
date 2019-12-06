SMTP_SERVICE_BLOCK = 'smtp-service'
SMTP_HOST = 'smtp_host'
SMTP_PORT = 'smtp_port'
SMTP_USERNAME = 'smtp_username'
SMTP_PASSWORD = 'smtp_password'
SMTP_USE_TLS = 'smtp_use_tls'
SMTP_LEVEL = 'smtp_level'

SMTP_DEFAULT_VALUES = {
    SMTP_HOST: '127.0.0.1',
    SMTP_PORT: '25',
    SMTP_USERNAME: None,
    SMTP_PASSWORD: None,
    SMTP_USE_TLS: True,
    SMTP_LEVEL: 0,
}

SMTP_CONFIG = [
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_USE_TLS,
    SMTP_LEVEL,
]

FILENAME = 'filename'
BUFFERED_CONTENT = 'buffered_content'
