import os

if not 'DB_PASSWORD' in os.environ:
    os.environ['DB_PASSWORD'] = 'dummypassword'
