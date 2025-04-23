# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import defaults

# Settings for deployment

from os import environ
from os.path import join, dirname, exists

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))

PRAKTOMAT_ID = environ['COMPOSE_PROJECT_NAME']

SITE_NAME = environ['PRAKTOMAT_NAME']
MIRROR = False

USING_ISABELLE = False

# The URL where this site is reachable. 'http://localhost:443/' in case of the
# development server.
BASE_HOST = 'http://' + environ['PRAKTOMAT_DOMAIN'] + ':443'
BASE_PATH = '/' + PRAKTOMAT_ID + '/'

ALLOWED_HOSTS = ['*', ]

# URL to use when referring to static files.
# STATIC_URL = BASE_PATH + 'static/'
# STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")


# STATIC_URL now defined in settings/defaults.py
# STATIC_ROOT now defined in settings/defaults.py

TEST_MAXLOGSIZE = 512

TEST_MAXFILESIZE = 512*1024

TEST_TIMEOUT = 120
TEST_MAXMEM = 1000

TEST_MAXFILENUMBER = 8192

# Saving an attestation for a solution with a lot of files might fail with the
# default value of 1000.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

# Example: "/home/media/media.lawrence.com/"
UPLOAD_ROOT = join(dirname(PRAKTOMAT_PATH), "work-data/")


ADMINS = [
    ('Praktomat Administrator', environ.get('PRAKTOMAT_ADMIN'))
]

SERVER_EMAIL = environ.get('PRAKTOMAT_ADMIN')


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = join(UPLOAD_ROOT, "sent-mails")

DEFAULT_FROM_EMAIL = environ.get('PRAKTOMAT_ADMIN')

DEBUG = MIRROR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':   environ.get('POSTGRES_USER'),
        'USER':   environ.get('POSTGRES_USER'),
        'PASSWORD':   environ.get('POSTGRES_PASSWORD'),
        'HOST':   environ.get('POSTGRES_HOST'),
        'PORT':   environ.get('POSTGRES_PORT')
    }
}

db_pass = environ.get('POSTGRES_PASSWORD')
if db_pass and exists(db_pass):
    with open(db_pass) as f:
        DATABASES['default']['PASSWORD'] = f.read()

# on linux command line  create database and databaseuser
# sudo -u postgres -P <db_user>
# sudo -u postgres -P praktomat
#
# sudo -u postgres createdb -O <db_user> <db_name>
# sudo -u postgres createdb -O praktomat praktomat_2017s

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SECRET_KEY gets generated via defaults.py

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'
CERTIFICATE = '/srv/praktomat/mailsign/signer.pem'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Enable Shibboleth:
SHIB_ENABLED = False

# Set this to False to disable registration via the website, e.g. when Single Sign On is used
if environ.get('PRAKTOMAT_LDAP', 'false').lower() == 'true':
    REGISTRATION_POSSIBLE = False
    LDAP_ENABLED = True
    LDAP_URI = "ldaps://ldap.uni-regensburg.de"
    LDAP_BASE = "o=uni-regensburg,c=de"
    DUMMY_MAT_NUMBERS = True
    ACCOUNT_CHANGE_POSSIBLE = False
else:
    LDAP_ENABLED = False
    REGISTRATION_POSSIBLE = True

SYSADMIN_MOTD_URL = None

# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = True

# It is recomendet to use DOCKER and not a tester account

# Use docker to test submission
USESAFEDOCKER = False
# DOCKER_IMAGE_NAME = environ.get('PRAKTOMAT_CHECKER_IMAGE')
# DOCKER_CONTAINER_WRITABLE = environ.get('PRAKTOMAT_CHECKER_WRITABLE', 'False') == 'True'
# DOCKER_UID_MOD = environ.get('PRAKTOMAT_CHECKER_UID_MOD') == 'True'
# DOCKER_CONTAINER_EXTERNAL_DIR = environ.get('PRAKTOMAT_CHECKER_EXTERNAL_DIR')
# DOCKER_CONTAINER_HOST_NET = environ.get('PRAKTOMAT_CHECKER_ENABLE_NETWORK') == 'True'
# DOCKER_DISCARD_ARTEFACTS = True

# Linux User "tester" and Usergroup "praktomat"
# Enable to run all scripts (checker) as the unix user 'tester'.
# Therefore put 'tester' as well as the Apache user '_www' (and your development user account)
# into a new group called "praktomat".

# Also edit your sudoers file with "sudo visudo -f /etc/sudoers.d/praktomat-tester".
# Add the following lines to the end of the file to allow the execution of
# commands with the user 'tester' without requiring a password:
# "_www		ALL=(tester) NOPASSWD: ALL"
# "developer	ALL=(tester) NOPASSWD: ALL"

# If you want to switch between "testuser" and "Docker"
# use "sudo visudo -f /etc/sudoers.d/praktomat-tester"
# "_www		ALL=(tester) NOPASSWD: ALL"
# "developer	ALL=(tester) NOPASSWD: ALL"
# "praktomat 	ALL=(tester) NOPASSWD: ALL"
#
# be sure that you change file permission
# sudo chown praktomat:tester praktomat/src/checker/scripts/java
# sudo chown praktomat:tester praktomat/src/checker/scripts/javac
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/java
# sudo chmod u+x,g+x,o-x praktomat/src/checker/scripts/javac


# Does Apache use "mod_xsendfile" version 1.0?
# If you use "libapache2-mod-xsendfile", this flag needs to be set to False
MOD_XSENDFILE_V1_0 = False

# Our VM has 4 cores, so lets try to use them
# But Gradle has a common build directory for a project
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 4
# But not with Isabelle, which is memory bound
if USING_ISABELLE:
    NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 1


# Various extra files and versions
JPLAGJAR = '/opt/praktomat-addons/jplag.jar'
CHECKSTYLEALLJAR = '/opt/praktomat-addons/checkstyle.jar'

LANG = "en_US.UTF-8"
LANGUAGE = "en_US:en"

MIMETYPE_ADDITIONAL_EXTENSIONS = \
    [("application/x-iml", ".iml"),
     ("application/yaml", ".yml"),
     ("application/yaml", ".yaml"),
     ("text/plain", ".lark"),
     ("text/plain", ".properties"),
     ("text/x-gradle", ".gradle"),
     ("text/x-gradle", ".gradle.kts"),
     ("text/x-isabelle", ".thy"),
     ("text/x-lean", ".lean"),
     ("text/x-log", ".log"),
     ("text/x-r-script", ".R"),
     ("text/x-python", ".py")]

# There's something fishy with the maximum file size set via ulimit
# We set it to a large value to avoid problems with the Haskell checker
TEST_MAXFILESIZE = 1000000000

# Finally load defaults for missing settings.
defaults.load_defaults(globals())
