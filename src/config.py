import os
import sys

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
    
PROJECT_ROOT = get_app_dir()

def default_ashita_root():
    return os.path.abspath(os.path.join(PROJECT_ROOT, "Ashita-v4beta-main"))

ASHITA_ROOT = default_ashita_root()

ASHITA_DOWNLOAD_URL = "https://github.com/AshitaXI/Ashita-v4beta/archive/refs/heads/main.zip"
ASHITA_DOWNLOADS_DIR = os.path.join(PROJECT_ROOT, "downloads")

ASHITA_ADDONS_DIR = os.path.join(ASHITA_ROOT, "addons")
ASHITA_PLUGINS_DIR = os.path.join(ASHITA_ROOT, "plugins")
ASHITA_SCRIPTS_DIR = os.path.join(ASHITA_ROOT, "scripts")

ASHITA_CONFIG_DIR = os.path.join(ASHITA_ROOT, "config")

ASHITA_BOOT_CONFIG_DIR = os.path.join(ASHITA_CONFIG_DIR, "boot")
ASHITA_ADDON_CONFIG_DIR = os.path.join(ASHITA_CONFIG_DIR, "addons")

PROFILE_NAME_DEFAULT = "MyProfile.ini"

REPOS_DIR = os.path.join(os.path.dirname(__file__), "repos")
