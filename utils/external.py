from os.path import dirname, abspath

def __setup_django(root_path, settings):
    import os
    import django
    import sys
    os.chdir(root_path)
    sys.path.append(root_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    django.setup()

# find main folder of python
PROJECT_PATH = dirname(dirname(abspath(__file__)))
# setting file
PROJECT_SETTING = "dolphin.settings"
# setup django
__setup_django(PROJECT_PATH, PROJECT_SETTING)