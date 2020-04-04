import logging
import os
import uuid

logger = logging.getLogger(__name__)


def get_file_path_folder(instance, folder_name, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    filepath = os.path.join(folder_name, filename)
    logger.debug(f'get_file_path_folder: {filepath}')
    return filepath

