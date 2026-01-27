import hashlib
import json

def compute_file_hash(file_bytes: bytes) -> str:
    """Compute SHA-256 hash of file content."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()

def compute_schema_hash(schema: dict) -> str:
    """Compute SHA-256 hash of a dictionary (sorted keys)."""
    # Sort keys to ensure consistent hash for same JSON content
    schema_str = json.dumps(schema, sort_keys=True)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(schema_str.encode('utf-8'))
    return sha256_hash.hexdigest()
