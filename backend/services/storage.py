"""
Favorites Storage Service for Cypher
Persists favorite hall ticket numbers to a JSON file
"""

import json
import os
from datetime import datetime, timezone

from core.logger import setup_logger

logger = setup_logger('storage')

FAVORITES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', 'data', 'favorites.json'
)


class FavoritesStorage:
    """Simple JSON-file backed storage for favorite hall tickets."""

    def __init__(self, filepath: str = FAVORITES_FILE):
        self.filepath = os.path.abspath(filepath)
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self._write([])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read(self) -> list:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Could not read favorites file, resetting: {exc}")
            return []

    def _write(self, favorites: list) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, indent=2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_favorites(self) -> list:
        """Return list of saved favorites (each is a dict with hallTicket + label)."""
        return self._read()

    def add_favorite(self, hall_ticket: str, label: str = '') -> dict:
        """
        Add a hall ticket to favorites.
        Returns the new favorite entry, or the existing one if already saved.
        """
        favorites = self._read()
        for entry in favorites:
            if entry.get('hallTicket', '').upper() == hall_ticket.upper():
                return entry  # Already exists

        entry = {
            'hallTicket': hall_ticket.upper(),
            'label': label or hall_ticket.upper(),
            'savedAt': datetime.now(timezone.utc).isoformat(),
        }
        favorites.append(entry)
        self._write(favorites)
        logger.info(f"Added favorite: {hall_ticket}")
        return entry

    def remove_favorite(self, hall_ticket: str) -> bool:
        """
        Remove a hall ticket from favorites.
        Returns True if it was found and removed, False otherwise.
        """
        favorites = self._read()
        new_favorites = [
            e for e in favorites
            if e.get('hallTicket', '').upper() != hall_ticket.upper()
        ]
        if len(new_favorites) == len(favorites):
            return False
        self._write(new_favorites)
        logger.info(f"Removed favorite: {hall_ticket}")
        return True

    def is_favorite(self, hall_ticket: str) -> bool:
        """Check whether a hall ticket is saved as a favorite."""
        favorites = self._read()
        return any(
            e.get('hallTicket', '').upper() == hall_ticket.upper()
            for e in favorites
        )
