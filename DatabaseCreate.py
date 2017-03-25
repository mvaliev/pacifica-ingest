#!/usr/bin/python
"""Create the database for ingest state."""
from ingest.orm import IngestState


def create_tables():
    """Create the ingest state table."""
    if not IngestState.table_exists():
        IngestState.create_table()


if __name__ == '__main__':
    create_tables()
