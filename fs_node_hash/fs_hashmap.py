from .tree_walker import fs_tree_recursion
from .file_hashing_tool import calc_file_hash, calc_dir_hash, register_hash_in_dict


def fs_tree_recursive_hash_map(node_path: str, data_arguments: dict = {}):

    # All children are evaluated, when evaluating a node
    mode = 'depth'

    duplicate_hashes = []

    def process_leaf(path: str):

        hash = calc_file_hash(path)
        file_metric = {
            'path': path,
            'hash': hash
        }
        register_hash_in_dict(hash, data_arguments, file_metric, duplicate_hashes=duplicate_hashes)
        return file_metric

    # children = [results of process_leaf]
    def process_node(path: str, children: list):

        children_hash_list = list(map(lambda child: child['hash'], children))
        hash = calc_dir_hash(children_hash_list)

        dir_metric = {
            'path': path,
            'hash': hash,
            'children': len(children_hash_list)
        }

        register_hash_in_dict(hash, data_arguments, dir_metric, duplicate_hashes=duplicate_hashes)

        return dir_metric

    process_functions = {
        'process_node': process_node,
        'process_leaf': process_leaf
    }
    result = fs_tree_recursion(node_path, process_functions, mode=mode)
    return data_arguments, duplicate_hashes


# print_fs_tree_recursion('/home/pmarkus/Downloads/Assignment2/TASK3/', mode='iter')
# print_fs_tree_recursion('/home/pmarkus/Downloads/Assignment2/TASK3/', mode='depth')
# print_fs_tree_recursion('/home/pmarkus/Downloads/Assignment2/TASK3/', mode='breadth')
# data_store = {}
# result_tree = print_fs_tree_recursive_store('/home/pmarkus/Downloads/Assignment2/TASK3/', data_arguments=data_store)

# result_hash_map, duplicate_hashes = fs_tree_recursive_hash_map('/home/pmarkus/Downloads/Assignment2/TASK3/', data_arguments=data_store)

# import pprint
# pprint.pprint(data_store)
# pprint.pprint(result_hash_map)

# python3 deduplication-tools/duplicate-processor/tree-walker.py
