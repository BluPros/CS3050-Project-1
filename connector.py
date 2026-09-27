"""Establishes a connection to the Firestore using the credntials
file on your local machine."""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from consts import CREDS_FILE

class FirebaseConnector:

    def __init__(self):
        cred = credentials.Certificate(CREDS_FILE)

        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    # get_database() returns a clean firestore.client object so that
    # methods may be easily performed directly on the client
    def get_database(self):
        return self.db
