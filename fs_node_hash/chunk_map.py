import hashlib
from .hash_buffer import hash_buffer
from .file_hashing import default_chunk_block_size_bytes


# Not tested
# For chunk level deduplication
def sort_file_chunks_in_chunk_map(
        chunk_map: dict,
        file_path: str,
        chunk_block_size_bytes: int = default_chunk_block_size_bytes):

    try:
        with open(file_path, "r") as text_file:
            for line in text_file:
                hash = hash_buffer(line.strip())
                chunk_map[hash] = len(line.encode('utf-8'))
    except UnicodeDecodeError:
        is_binary_file = True

    if (is_binary_file):

        with open(file_path, "rb") as file:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: file.read(chunk_block_size_bytes), b""):
                sha256_hash = hashlib.sha256()
                sha256_hash.update(byte_block)
                sha256_hash.hexdigest()

                chunk_map[sha256_hash] = file_path
