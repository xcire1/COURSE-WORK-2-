from datetime import datetime
from pathlib import Path
import sqlite3
import pandas as pd

from app.data.db import connect_database
from app.data import datasets_metadata   # must contain path to tickets DB

#     CONSTANTS

VALID_PRIORITIES = ['Low', 'Medium', 'High', 'Urgent']
VALID_TICKET_STATUS = ['Open', 'In Progress', 'Waiting', 'Resolved', 'Closed']

#     VALIDATION

def validate_ticket_fields(title, description, priority, status, created_by):
    """Validate ticket fields before insert/update."""

    if not all([title, description, priority, status, created_by]):
        raise ValueError("All fields except 'assigned_to' are required.")

    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}.")

    if status not in VALID_TICKET_STATUS:
        raise ValueError(f"Status must be one of {VALID_TICKET_STATUS}.")

#     CRUD OPERATIONS

def create_ticket(title, description, priority, status, created_by, assigned_to=None):
    """Create a new ticket."""
    
    validate_ticket_fields(title, description, priority, status, created_by)

    conn = connect_database(db_path=datasets_metadata.tickets)
    cursor = conn.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO tickets
        (title, description, priority, status, created_by, assigned_to, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, priority, status, created_by, assigned_to, created_at))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id


def get_all_tickets():
    """Return all tickets as a DataFrame."""
    conn = connect_database(db_path=datasets_metadata.tickets)
    df = pd.read_sql_query(
        "SELECT * FROM tickets ORDER BY id DESC", conn
    )
    conn.close()
    return df


def get_ticket_by_id(ticket_id):
    """Return a single ticket."""
    conn = connect_database(db_path=datasets_metadata.tickets)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()

    return row


def update_ticket(ticket_id, title, description, priority, status, created_by, assigned_to=None):
    """Update ticket details."""

    validate_ticket_fields(title, description, priority, status, created_by)

    conn = connect_database(db_path=datasets_metadata.tickets)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET title = ?, description = ?, priority = ?, status = ?, created_by = ?, assigned_to = ?
        WHERE id = ?
    """, (title, description, priority, status, created_by, assigned_to, ticket_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0  # True = updated, False = not found


def update_ticket_status(ticket_id, new_status):
    """Update only the ticket status."""

    if new_status not in VALID_TICKET_STATUS:
        raise ValueError(f"Status must be one of {VALID_TICKET_STATUS}.")

    conn = connect_database(db_path=datasets_metadata.tickets)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE id = ?
    """, (new_status, ticket_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0


def delete_ticket(ticket_id):
    """Delete a ticket permanently."""
    conn = connect_database(db_path=datasets_metadata.tickets)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted > 0
