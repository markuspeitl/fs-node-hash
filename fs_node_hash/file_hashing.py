import hashlib
import os
import math


# 4KB
default_chunk_block_size_bytes = 4096


def calc_file_hash(
        path: str,
        blocks_limit=-1,
        chunk_block_size_bytes=default_chunk_block_size_bytes) -> str:

    sha256_hash = hashlib.sha256()
    with open(path, "rb") as file_stream:

        size_bytes = os.fstat(file_stream.fileno()).st_size
        blocks_in_file = math.ceil(size_bytes/chunk_block_size_bytes)

        if (blocks_limit > 0):
            blocks_in_file = blocks_limit

        for _ in range(0, blocks_in_file):

            byte_block = file_stream.read(chunk_block_size_bytes)
            sha256_hash.update(byte_block)

        # Read and update hash string value in blocks of 4K
        # for byte_block in iter(lambda: file_stream.read(chunk_block_size_bytes), b""):
        #    sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()

# Hashing quickly becomes the performance bottleneck for big files -> therefore we can improve performance by taking
# samples across a file, which should still provide a VERY good indication whether the file is the same as another


def sample_file_hash(
        path: str,
        samples_cnt: int,
        blocks_per_sample: int,
        chunk_block_size_bytes=default_chunk_block_size_bytes):

    sha256_hash = hashlib.sha256()
    with open(path, "rb") as file_stream:

        size_bytes = os.fstat(file_stream.fileno()).st_size
        if (size_bytes <= samples_cnt * blocks_per_sample * chunk_block_size_bytes):
            return calc_file_hash(path)

        blocks_in_file = math.ceil(size_bytes/chunk_block_size_bytes)

        blocks_betweenn_samples = blocks_in_file / samples_cnt

        for sample_index in range(0, samples_cnt):
            current_center = int(blocks_betweenn_samples * sample_index)

            range_start = int(current_center - blocks_per_sample / 2)
            if (range_start < 0):
                range_start = 0

            file_stream.seek(range_start)

            for _ in range(0, blocks_per_sample):
                byte_block = file_stream.read(chunk_block_size_bytes)
                sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()
