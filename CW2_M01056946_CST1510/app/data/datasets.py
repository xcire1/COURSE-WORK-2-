from datetime import datetime
from pathlib import Path
import sqlite3
import pandas as pd

from app.data.db import connect_database
from app.data import datasets_metadata    # contains db paths

#     CONSTANTS

VALID_DATASET_TYPES = ["csv", "excel", "json", "sqlite", "parquet"]
VALID_DATASET_STATUS = ["Active", "Archived", "Deprecated"]

#     VALIDATION

def validate_dataset_fields(name, dataset_type, file_path, status):
    """Validate dataset fields."""

    if not all([name, dataset_type, file_path, status]):
        raise ValueError("Name, dataset_type, file_path, and status are required.")

    if dataset_type not in VALID_DATASET_TYPES:
        raise ValueError(f"dataset_type must be one of {VALID_DATASET_TYPES}")

    if status not in VALID_DATASET_STATUS:
        raise ValueError(f"status must be one of {VALID_DATASET_STATUS}")

    if not Path(file_path).exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")


#     CRUD OPERATIONS

def register_dataset(name, dataset_type, file_path, status="Active", description=None, created_by=None):
    """Register a new dataset in the database."""
    validate_dataset_fields(name, dataset_type, file_path, status)

    created_at = datetime.now().isoformat()

    conn = connect_database(db_path=datasets_metadata.datasets)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets
        (name, dataset_type, file_path, status, description, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dataset_type, file_path, status, description, created_by, created_at))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id


def get_all_datasets():
    """Return all datasets as a DataFrame."""
    conn = connect_database(db_path=datasets_metadata.datasets)
    df = pd.read_sql_query(
        "SELECT * FROM datasets ORDER BY id DESC", conn
    )
    conn.close()
    return df


def get_dataset_by_id(dataset_id):
    """Return a specific dataset."""
    conn = connect_database(db_path=datasets_metadata.datasets)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM datasets WHERE id = ?", (dataset_id,))
    row = cursor.fetchone()

    conn.close()
    return row


def update_dataset(dataset_id, name, dataset_type, file_path, status="Active", description=None, created_by=None):
    """Update dataset metadata."""

    validate_dataset_fields(name, dataset_type, file_path, status)

    conn = connect_database(db_path=datasets_metadata.datasets)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE datasets
        SET name = ?, dataset_type = ?, file_path = ?, status = ?, description = ?, created_by = ?
        WHERE id = ?
    """, (name, dataset_type, file_path, status, description, created_by, dataset_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0   # True if updated


def update_dataset_status(dataset_id, new_status):
    """Update a dataset's status only."""
    if new_status not in VALID_DATASET_STATUS:
        raise ValueError(f"Status must be one of {VALID_DATASET_STATUS}")

    conn = connect_database(db_path=datasets_metadata.datasets)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE datasets
        SET status = ?
        WHERE id = ?
    """, (new_status, dataset_id))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0


def delete_dataset(dataset_id):
    """Remove a dataset record."""
    conn = connect_database(db_path=datasets_metadata.datasets)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM datasets WHERE id = ?", (dataset_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted > 0

#     EXTRA FEATURES

def load_dataset_to_dataframe(dataset_id):
    """Automatically load a dataset into a pandas DataFrame based on its type."""

    dataset = get_dataset_by_id(dataset_id)
    if not dataset:
        raise ValueError(f"Dataset ID {dataset_id} not found.")

    _, name, dataset_type, file_path, status, description, created_by, created_at = dataset

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found at {file_path}")

    # Load depending on type
    if dataset_type == "csv":
        return pd.read_csv(file_path)

    if dataset_type == "excel":
        return pd.read_excel(file_path)

    if dataset_type == "json":
        return pd.read_json(file_path)

    if dataset_type == "sqlite":
        conn = sqlite3.connect(file_path)
        df = pd.read_sql_query("SELECT * FROM data", conn)
        conn.close()
        return df

    if dataset_type == "parquet":
        return pd.read_parquet(file_path)

    raise ValueError(f"Unsupported dataset type: {dataset_type}")
