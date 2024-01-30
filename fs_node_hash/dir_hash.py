
from .hash_buffer import hash_buffer


def calc_dir_hash(children_hash_list: list):
    sorted_child_hashes = sorted(children_hash_list)
    children_signature = ('').join(sorted_child_hashes)
    dir_hash = hash_buffer(children_signature)
    return dir_hash
