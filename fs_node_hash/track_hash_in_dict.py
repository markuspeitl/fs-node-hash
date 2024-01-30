from typing import Any
from .file_hashing import calc_file_hash, sample_file_hash


def hash_file_to_dict(path: str, hash_dict: dict, storage_content: dict, duplicate_hashes: list = None):
    hash = calc_file_hash(path)
    register_hash_in_dict(hash, hash_dict, storage_content, duplicate_hashes)
    return hash


def register_hash_in_dict(hash_value: str, hash_dict: dict, storage_content: dict, duplicate_hashes: list = None):
    if hash_value in hash_dict:
        hash_dict[hash_value].append(storage_content)

        if duplicate_hashes is not None and hash_value not in duplicate_hashes:
            duplicate_hashes.append(hash_value)
            print("Found duplicate: " + hash_value)
            print(storage_content)

    else:
        hash_dict[hash_value] = [storage_content]


def register_detect_collision(key: Any, collision_dict: dict, target_value: Any) -> bool:
    if not key in collision_dict:
        collision_dict[key] = target_value
        print(f"Registering entry in collision_dict at: {key}")
        return False

    print(f"collision: {key}")
    return True


def register_file_hash_check_collision(file_path: str, hash_dict: dict, storage_content=None, blocks_limit=-1):
    # file_hash = calc_file_hash(file_path, blocks_limit=blocks_limit)
    file_hash = sample_file_hash(file_path, 20, 4)
    return register_detect_collision(file_hash, hash_dict, storage_content)
