import os

"""
Utility functions for getting paths to directories and files.

Functions:
    get_path(target_dir)
    search_tree(root, target)
    get_image_path(image_name)

Variables:
    easycut_path
    tests_path
    asmcnc_path
    skava_ui_img_path

Usage:
    from asmcnc.core_UI import path_utils
    
    path = get_path("easycut-smartbench")
    image_path = get_image_path("image.png")
    
    print(easycut_path)
    print(tests_path)
    print(asmcnc_path)
    print(skava_ui_img_path)
"""

def get_path(target_dir):
    """
    Returns the path to the target directory or file (first instance found only).

    Args:
        target_dir (str): The target directory.

    Returns:
        str: The path to the target directory.
    """
    
    root_path = os.path.abspath(__file__)  # Get the absolute path of the current script

    try:
        # Quick serach in the path of current script
        target_path_index = root_path.index(target_dir)
        target_path = root_path[:target_path_index + len(target_dir)]
        return target_path
    except ValueError:
        # If not found, search the whole tree
        try:
            target_path = search_tree(easycut_path, target_dir)
            return target_path
        except:
            print("Error: '{}' not found in the path '{}'.".format(target_dir, root_path))
            return None
    
def search_tree(root, target):
    """
    Search for a target file or folder within a directory tree.

    Parameters:
    root (str): The root directory to start the search from.
    target (str): The name of the file or folder to search for.

    Returns:
    str: The path of the target file or folder if found, None otherwise.
    """
    search_results = []

    for foldername, _, filenames in os.walk(root):
        if target in foldername:
            search_results.append(foldername)
        elif target in filenames:
            search_results.append(os.path.join(foldername, target))

    if not search_results:
        print("Error: '{}' not found in the path '{}'.".format(target, root))    
        return None
    return search_results[0] if len(search_results) == 1 else search_results

def get_image_path(image_name):
    """
    Returns the full path of an image given its name.
    Only works for images in the skavaUI/img directory.

    Args:
        image_name (str): The name of the image.

    Returns:
        str: The full path of the image.
    """
    return os.path.join(skava_ui_img_path, image_name)
    
# Common paths
easycut_path = get_path("easycut-smartbench") # easycut-smartbench
tests_path = get_path("tests") # easycut-smartbench/tests
asmcnc_path = get_path("asmcnc") # easycut-smartbench/src/asmcnc
skava_ui_img_path = os.path.join(asmcnc_path, "skavaUI", "img") # easycut-smartbench/src/asmcnc/skavaUI/img
