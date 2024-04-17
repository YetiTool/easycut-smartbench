import os
import re

from asmcnc.comms.logging_system.logging_system import Logger

"""
Utility functions for getting paths to directories and files.
This file must remain somewhere within /easycut-smartbench/
Root for all searches is 1 stage up from /easycut-smartbench/

Functions:
    get_path(target_dir, files_only=False, folders_only=False, first_result_only=False, search_outside_easycut=False)
    search_tree(root, target, files_only=False, folders_only=False, first_result_only=False)
    join(folder, filename)

Variables:
    easycut_path
    tests_path
    asmcnc_path
    skava_ui_path
    skava_ui_img_path


Usage:
    # Import path_utils
    from asmcnc.core_UI import path_utils
    
    # Get the path of a directory or  an existing file
    path = get_path("easycut-smartbench")
    path = get_path("tests", folders_only=True, first_result_only=True)
    path = get_path("z_probe.png", files_only=True)
    path = get_path("path_utils.py")
    path = get_path("plus.txt", search_outside_easycut=True)
    etc.
    
    # To create a path to a file that might not exist yet:
    path = join(get_path("sb_values"),"model_info.json"))
    
    # Common paths
    print(easycut_path)
    print(tests_path)
    print(asmcnc_path)
    print(skava_ui_path)
    print(skava_ui_img_path)
    print(sb_values_path)
"""

def get_path(target_dir, files_only=False, folders_only=False, first_result_only=False, search_outside_easycut=False):
    """
    Returns the whole path(s) of the target directory or file.

    Args:
        target_dir (str): The target directory.

    Kwargs:
        files_only (bool): If True, only search for files.
        folders_only (bool): If True, only search for folders.
        first_result_only (bool): If True, return the first result only.
        search_outside_easycut (bool): If True, search from parent of easycut

    Returns:
        str: If one path is found, the entire path of the target directory or file.
        list: If multiple paths are found, a list of the paths to the found directories or files.
    """

    if files_only and folders_only:
        raise ValueError("Both 'files_only' and 'folders_only' cannot be True at the same time.")

    root_path = os.path.abspath(__file__)  # Get the absolute path of the current script

    try:
        # Quick search in the path of current script
        if not files_only:
            target_path_index = root_path.index(target_dir)
            target_path = root_path[:target_path_index + len(target_dir)]
            return target_path.replace("\\", "/")
        else:
            raise ValueError
    except ValueError:
        # If not found, search the whole tree
        try:
            if search_outside_easycut:
                easycut_location = os.path.dirname(easycut_path) # Get location of easycut folder
                root = easycut_location
            else:
                root = easycut_path
            target_path = search_tree(root, target_dir, files_only, folders_only, first_result_only)
            return target_path
        except:
            Logger.info("Error: '{}' not found in the path '{}'.".format(target_dir, root_path))
            return None
    
def search_tree(root, target, files_only=False, folders_only=False, first_result_only=False):
    """
    Search for a target file or folder within a directory tree.

    Args:
        root (str): The root directory to start the search from.
        target (str): The name of the file or folder to search for.

    Kwargs:
        files_only (bool): If True, only search for files.
        folders_only (bool): If True, only search for folders.
        first_result_only (bool): If True, return the first result only.

    Returns:
        str: The path of the target file(s) or folder(s) if found, None otherwise.
    """
    search_results = []

    target_split = re.split(r'[\\/]|' + re.escape(os.sep), target) # split the target into a list of strings eg. ['skavaUI', 'img']
    target_slash_count = len(target_split) - 1

    for foldername, _, filenames in os.walk(root):
        folder_path_split = re.split(r'[\\/]|' + re.escape(os.sep), foldername) # split the foldername into a list of strings eg. ['easycut-smartbench', 'src', 'asmcnc', 'skavaUI', 'img']

        if target_slash_count == 0:
            if target in filenames and not folders_only: # If target found as a file
                search_results.append(foldername + "/" + target)
            elif target in folder_path_split[-1] and not files_only: # If target found as a folder
                search_results.append(foldername)
        else:
            if target_split == folder_path_split[-len(target_split):] and not files_only: # If target found as a folder where target is a path eg. 'skavaUI/img'
                search_results.append(foldername)
            elif target_split[:-1] == folder_path_split[-len(target_split)+1:] and target_split[-1] in filenames and not folders_only: # If target found as a file where target is a path eg. 'skavaUI/img/z_probe.png'
                search_results.append(foldername + "/" + target_split[-1])


    if not search_results:
        Logger.info("Error: '{}' not found in the path '{}'.".format(target, root))
        return None
    
    # Tidy output
    search_results = [result.replace("\\", "/") for result in search_results]

    return search_results[0] if (len(search_results) == 1  or first_result_only) else search_results


def join(folder, filename):
    """
    Returns the path with the given folder and filename.
    Can be used for filepaths that don't exist yet.
    """
    return os.path.join(folder, filename).replace("\\", "/")
# Common paths
easycut_path = get_path("easycut-smartbench") # easycut-smartbench
root_tests_path = get_path("easycut-smartbench/tests") # easycut-smartbench/tests
asmcnc_path = get_path("asmcnc") # easycut-smartbench/src/asmcnc
skava_ui_path = get_path("skavaUI") # easycut-smartbench/src/asmcnc/skavaUI
skava_ui_img_path = get_path("skavaUI/img") # easycut-smartbench/src/asmcnc/skavaUI/img
sb_values_path = get_path("sb_values")  # easycut-smartbench/src/sb_values