"""Connect to Firebase Cloud Firestore and perform database operations."""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from consts import COLLECTION_NAME
from consts import CREDS_FILE


class FirebaseConnector:
    """Encapsulates Firebase authentication and Steam game collection access."""

    db = None

    def __init__(self):
        """Initialize Firebase once and create a Firestore client."""
        if FirebaseConnector.db is None:
            if not firebase_admin._apps:
                credential = credentials.Certificate(CREDS_FILE)
                firebase_admin.initialize_app(credential)

            FirebaseConnector.db = firestore.client()

        self.collection = FirebaseConnector.db.collection(COLLECTION_NAME)

    def get_database(self):
        """Return the Firestore client when a caller genuinely needs it."""
        return FirebaseConnector.db

    def delete_all_games(self):
        """Delete every document in the Steam games collection."""
        for document in self.collection.stream():
            document.reference.delete()

    def upload_game(self, game_data):
        """Upload one game document, using the Steam app ID as its document ID."""
        document_id = str(game_data["app_id"])
        self.collection.document(document_id).set(game_data)

    def execute_single_filter(self, field, operator, value):
        """Return document dictionaries matching one query condition."""
        query = self.collection.where(
            filter=firestore.FieldFilter(field, operator, value)
        )

        return [
            document.to_dict()
            for document in query.stream()
        ]

    def execute_two_and_filters(
        self,
        first_field,
        first_operator,
        first_value,
        second_field,
        second_operator,
        second_value,
    ):
        """Return document dictionaries matching both query conditions."""
        query = self.collection.where(
            filter=firestore.FieldFilter(
                first_field,
                first_operator,
                first_value,
            )
        ).where(
            filter=firestore.FieldFilter(
                second_field,
                second_operator,
                second_value,
            )
        )

        return [
            document.to_dict()
            for document in query.stream()
        ]