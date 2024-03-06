import os

"""
Utility functions for getting paths to directories and files.
This folder must remain somewhere within /easycut-smartbench/

Functions:
    get_path(target_dir, files_only=False, folders_only=False, first_result_only=False)
    search_tree(root, target, files_only=False, folders_only=False, first_result_only=False)

Variables:
    easycut_path
    tests_path
    asmcnc_path
    skava_ui_path
    skava_ui_img_path


Usage:
    # Import path_utils
    from asmcnc.core_UI import path_utils
    
    # Get the path of a directory or file
    path = get_path("easycut-smartbench")
    path = get_path("tests", folders_only=True, first_result_only=True)
    path = get_path("z_probe.png", files_only=True)
    path = get_path("path_utils.py")
    etc.
    
    # Common paths
    print(easycut_path)
    print(tests_path)
    print(asmcnc_path)
    print(skava_ui_path)
    print(skava_ui_img_path)
"""

def get_path(target_dir, files_only=False, folders_only=False, first_result_only=False):
    """
    Returns the whole path(s) of the target directory or file.

    Args:
        target_dir (str): The target directory.

    Kwargs:
        files_only (bool): If True, only search for files.
        folders_only (bool): If True, only search for folders.
        first_result_only (bool): If True, return the first result only.

    Returns:
        str: If one path is found, the entire path of the target directory or file.
        list: If multiple paths are found, a list of the paths to the found directories or files.
    """

    if files_only and folders_only:
        raise ValueError("Both 'files_only' and 'folders_only' cannot be True at the same time.")
    
    root_path = os.path.abspath(__file__)  # Get the absolute path of the current script

    try:
        # Quick serach in the path of current script
        if not files_only:
            target_path_index = root_path.index(target_dir)
            target_path = root_path[:target_path_index + len(target_dir)]
            return target_path
        else:
            raise ValueError
    except ValueError:
        # If not found, search the whole tree
        try:
            target_path = search_tree(easycut_path, target_dir, files_only, folders_only, first_result_only)
            return target_path
        except:
            print("Error: '{}' not found in the path '{}'.".format(target_dir, root_path))
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

    for foldername, _, filenames in os.walk(root):
        # If target is in foldername after the last slash
        if target in foldername.split(os.sep)[-1] and not files_only:
            search_results.append(foldername)
        elif target in filenames and not folders_only:
            search_results.append(os.path.join(foldername, target))

    if not search_results:
        print("Error: '{}' not found in the path '{}'.".format(target, root))    
        return None
    return search_results[0] if (len(search_results) == 1  or first_result_only) else search_results
    
# Common paths
easycut_path = get_path("easycut-smartbench") # easycut-smartbench
tests_path = get_path("tests") # easycut-smartbench/tests
asmcnc_path = get_path("asmcnc") # easycut-smartbench/src/asmcnc
skava_ui_path = get_path("skavaUI") # easycut-smartbench/src/asmcnc/skavaUI
skava_ui_img_path = os.path.join(asmcnc_path, "skavaUI", "img") # easycut-smartbench/src/asmcnc/skavaUI/img