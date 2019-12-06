from standard_logger.standard_logger import Logger
from .consts import *
import traceback
import toml


class Config(object):
    logger = Logger("simple_email.Config")
    CONFIG = {}

    @classmethod
    def parse_config(cls, config_file, splunk_config=None):
        try:
            with open(config_file) as f:
                toml_str = f.read()
            toml_data = toml.loads(toml_str)
            cls.parse_smtp_service(toml_data)
        except:
            msg = traceback.format_exc().splitlines()[-1]
            cls.logger.action('parse_config',
                   None,
                   'failed to parse {}: {}, '.format(config_file, msg))
            cls.parse_smtp_service(toml_data)

    @classmethod
    def parse_json(cls, json_data):
        cls.parse_smtp_service(json_data)
        
    @classmethod
    def get_value(cls, key, value=None):
        return cls.CONFIG.get(key, value)

    @classmethod
    def parse_smtp_service(cls, json_data, block_name=SMTP_SERVICE_BLOCK):
        block = json_data.get(SMTP_SERVICE_BLOCK, {})

        for k in SMTP_CONFIG:
            cls.CONFIG[k] = block.get(k, SMTP_DEFAULT_VALUES[k])
