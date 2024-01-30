from genericpath import exists, isfile
import os
from typing import Callable, TypedDict
from fs_node_hash.util import time_transient
from .dir_hashing import calc_dir_hash
from .file_hashing import sample_file_hash
from .track_hash_in_dict import register_hash_in_dict
from tree_utils.fs_recursion import RecursionStrategy, ProcessingFunctions, fs_tree_recursion


class NodeProcessedValue(TypedDict):
    path: str
    size: float
    child_cnt: int


HashToNodeValuesDict = dict[str, list[NodeProcessedValue]]
HashValuePair = tuple[str, NodeProcessedValue]


class NodeHashResults(TypedDict):
    files: HashToNodeValuesDict
    dirs: HashToNodeValuesDict


def init_hash_results(hash_results: NodeHashResults = {}):
    if (not hash_results):
        hash_results = {}

    if 'files' not in hash_results:
        hash_results['files'] = {}

    if 'dirs' not in hash_results:
        hash_results['dirs'] = {}

    return hash_results


_hash_file_samples_cnt_const = 20
_hash_file_block_cnt_const = 6


# Restore mtime and atime after hashing
sample_file_hash = time_transient(sample_file_hash)


def calc_file_hash_and_info(
        path: str,
        hash_to_info_dict: HashToNodeValuesDict,
        duplicate_hashes: list[str] = None) -> str:

    # In this case only samples 12 samples/file * 4 chunks/sample * 4096byts/chunk = 196KB of
    # data accross the file for creating the hash or returns a normal hash for smaller files
    # Note that these settings need to stay the same for the duplicate matching to work
    hash = sample_file_hash(path)
    # hash = fs_hashmap.calc_file_hash(path)
    processed_file_value: NodeProcessedValue = {
        'path': path,
        'size': os.stat(path).st_size
    }

    register_hash_in_dict(hash, hash_to_info_dict, processed_file_value, duplicate_hashes=duplicate_hashes)

    return hash


def calc_dir_hash_and_info(
        dir_path: str,
        children_paths: list[str],
        child_hashes: list[str],
        hash_to_info_dict: HashToNodeValuesDict,
        duplicate_hashes: list[str] = None) -> str:

    # size_sum = sum(map(lambda child_proc_res: child_proc_res['size'], children_processing_results))
    hash = calc_dir_hash(child_hashes)
    processed_dir_value: NodeProcessedValue = {
        'path': dir_path,
        "child_cnt": len(children_paths),
        'size': 0
    }

    register_hash_in_dict(hash, hash_to_info_dict, processed_dir_value, duplicate_hashes=duplicate_hashes)
    return hash


def sort_file_names(children_list: list[str]) -> list[str]:
    children_list.sort()
    return children_list


def calculate_dir_hash_index(
        node_path: str,
        hash_results: NodeHashResults = None,
        options={},
        mode=RecursionStrategy.BFS) -> tuple[NodeHashResults, list[str], list[str]]:

    hash_results = init_hash_results(hash_results)
    file_duplicate_hashes: list[str] = []
    dir_duplicate_hashes: list[str] = []

    node_processing_functions: ProcessingFunctions = ProcessingFunctions()

    file_hash_results: HashToNodeValuesDict = hash_results['files']
    dir_hash_results: HashToNodeValuesDict = hash_results['dirs']

    process_leaf: Callable[[str], str] = lambda path: calc_file_hash_and_info(path, file_hash_results, file_duplicate_hashes)
    process_node: Callable[[str, list[str], list[str]], str] = lambda path, child_paths, child_results: calc_dir_hash_and_info(path, child_paths, child_results, dir_hash_results, dir_duplicate_hashes)
    node_processing_functions.process_node = process_node
    node_processing_functions.process_leaf = process_leaf

    options['sort_fn'] = sort_file_names

    fs_tree_recursion(node_path, node_processing_functions, options=options, mode=mode)

    return hash_results, file_duplicate_hashes, dir_duplicate_hashes


# The result of this holds information about: hashes of descendants and self mapped to lists of values that represent duplicate data
def calculate_dir_or_file_hash_indexes(target_node_abs: str) -> HashToNodeValuesDict:

    if (os.path.isfile(target_node_abs)):

        file_hash_index: dict = {}
        calc_file_hash_and_info(target_node_abs, file_hash_index)
        return None, file_hash_index

    hash_results, _, _ = calculate_dir_hash_index(target_node_abs)
    dir_hash_index = hash_results['dirs']
    file_hash_index = hash_results['files']
    return dir_hash_index, file_hash_index


# Only use when not interested in descendant file hashes later
def calculate_file_or_dir_hash_values_pair(path: str) -> HashToNodeValuesDict:
    dir_hash_index, file_hash_index = calculate_dir_or_file_hash_indexes(path)

    if (isfile(path)):
        return next(iter(file_hash_index.items()))

    return next(iter(dir_hash_index.items()))


# Only use when not interested duplicate descendants in the passed node
def get_hash_value_pair_for(node_path: str) -> HashValuePair:  # source_home_path: str, target_home_path: str, rule_target_dir_rel: str
    if (not node_path or not exists(node_path)):
        raise Exception(f"Invalid node_path {node_path} - unable to hash non existing file -> has to be existing file")

    # dir_hash_index, file_hash_index = calculate_dir_or_file_hash_indexes(node_path)
    hash, hash_result_list = calculate_file_or_dir_hash_values_pair(node_path)

    return hash, hash_result_list[0]


def get_hash_value_pairs_for(source_paths: list[str]) -> list[HashValuePair]:
    return [get_hash_value_pair_for(source_path) for source_path in source_paths]
