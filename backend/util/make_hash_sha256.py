import json
import hashlib


def make_hash_sha256(*args):
    """
    Return a SHA-256 hash of given arguments
    """
    stringified_args = sorted(map(json.dumps, args))
    joined_data = "".join(stringified_args)

    return hashlib.sha256(joined_data.encode("utf-8")).hexdigest()
