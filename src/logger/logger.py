from logging import config, getLogger

from config import settings

config.fileConfig(f"{settings.root_path}/{settings.log.config_file_name}")

logger = getLogger(settings.log.logger_name)
