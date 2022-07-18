import os

if "DB_PASSWORD" not in os.environ:
    os.environ["DB_PASSWORD"] = "dummypassword"
