from utils.managers.manager import Manager
from utils.managers.template_manager import TemplateManager
import shutil
import os


class DownloadManager(Manager):

    @classmethod
    def get_project_archive(cls, project, compression):
        path = "{}{}\\{}\\".format(TemplateManager.ROOT_PATH, "out", project)
        archive_path = "{}{}".format(path, project)
        archive = "{}.{}".format(archive_path, compression)
        if os.path.exists(archive):
            shutil.rmtree(path=archive, ignore_errors=True)
        if compression == 'zip' or compression == 'tar':
            shutil.make_archive(archive_path, compression, "{}{}".format(path, "src"))
        if os.path.exists(archive):
            return archive
        else:
            return None
