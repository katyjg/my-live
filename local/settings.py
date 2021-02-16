DEBUG = True

# Local Timezone
TIME_ZONE = 'America/Regina'

# Internal Access Settings
TRUSTED_IPS = ['127.0.0.1/32']
TRUSTED_PROXIES = 1

# Downloads
RESTRICT_DOWNLOADS = False
DOWNLOAD_PROXY_URL = "http://vanilla-data/download"

# Shift parameters
HOURS_PER_SHIFT = 8

# Use Client Relations Management (Support Records/User Feedback)
LIMS_USE_CRM = False

# Use Access Control Lists
LIMS_USE_ACL = False

# Schedule App settings
LIMS_USE_SCHEDULE = False
MIN_SUPPORT_HOUR = 8
MAX_SUPPORT_HOUR = 22
SUPPORT_EMAIL = 'vanilla-support@email.ca'
FACILITY_MODES = "https://external.beam.mode.src"
""" FACILITY_MODES should reference an API that returns a JSON list containing a dictionary for each mode, with fields:
    - "start": string formatted date matching %Y-%m-%dT%H:%M:%SZ
    - "end": string formatted date matching %Y-%m-%dT%H:%M:%SZ
    - "kind": code to use for CSS class for styling (built-in codes include N, NS, D, X, M, MV, M0, MT, DS, DST, DS-CSR)
"""

# LDAP Authentication Settings:
LDAP_BASE_DN = 'dc=vanilla,dc=org'
LDAP_SERVER_URI = 'ldap.example.ca'
LDAP_MANAGER_DN = 'cn=Directory Manager'
LDAP_MANAGER_SECRET = 'ldap-password'
LDAP_USER_TABLE = 'ou=People'
LDAP_USER_ROOT = '/home'
LDAP_GROUP_TABLE = 'ou=Groups'
LDAP_USER_SHELL = '/bin/bash'
LDAP_SEND_EMAILS = False
LDAP_ADMIN_UIDS      = [1000]

# LDAP Authentication Settings
LDAP_AUTH_URL = "ldap://{}:389".format(LDAP_SERVER_URI)
LDAP_AUTH_SEARCH_BASE = "{},{}".format(LDAP_USER_TABLE, LDAP_BASE_DN)
LDAP_AUTH_OBJECT_CLASS = "posixAccount"
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
LDAP_AUTH_USE_TLS = True
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

def clean_user(user, data):
    # A function to clean up user data from ldap information

    names = data['gecos'][0].split(' ', 1)
    first_name = names[0].strip()
    last_name = "" if len(names) < 2 else names[1].strip()
    user_uids = set(map(int, data['gidnumber']))
    admin_uids = set(map(int, LDAP_ADMIN_UIDS))

    if user_uids & admin_uids:
        user.is_superuser = True
        user.is_staff = True

    if not user.name:
        user.name = user.username

    if (first_name, last_name) != (user.first_name, user.last_name):
        user.first_name = first_name
        user.last_name = last_name
    user.save()

LDAP_AUTH_SYNC_USER_RELATIONS = clean_user

# Database Config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vanilla',
        'USER': 'vanilla',
        'PASSWORD': 'CDAvxbkLnCQqb6bE0RCguPEpe2FOPN',
        'HOST': '172.19.0.2', # Run `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' deploy_database_1` in /deploy directory
        'PORT': '5432'
    }
}
