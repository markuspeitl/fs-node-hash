import hashlib


def hash_buffer(string_content: str) -> str:
    sha256_hash = hashlib.sha256()
    buffer = bytes(string_content, 'utf-8')
    sha256_hash.update(buffer)
    return sha256_hash.hexdigest()
