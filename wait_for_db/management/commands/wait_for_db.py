"""
Django command to wait for the database to be available.
"""

import time

from django.db.utils import OperationalError # type: ignore
from django.core.management.base import BaseCommand # type: ignore
from psycopg2 import OperationalError as Psycopg2OperationalError # type: ignore


class Command(BaseCommand):
    """Django command to wait for database container to be up."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write(f"Waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.stdout.write("Checking database...")
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, Psycopg2OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database ready."))