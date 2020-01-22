from backend.util.make_hash_sha256 import make_hash_sha256


def test_make_hash_sha256():
    correct_hash = "39a3e3552a8300b2b8cbb55f3d9aeff70746127a59f804f20cd9ce01250f234a"

    assert make_hash_sha256("text data", 42) == make_hash_sha256(42, "text data")
    assert make_hash_sha256("text data", 42) == correct_hash
