import os

def get_path(target_dir):
    """
    Returns the path to the target directory.

    Args:
        target_dir (str): The target directory.

    Returns:
        str: The path to the target directory.
    """
    
    root_path = os.path.abspath(__file__)  # Get the absolute path of the current script

    try:
        target_path_index = root_path.index(target_dir)
        target_path = root_path[:target_path_index + len(target_dir)]
        return target_path
    except ValueError:
        print("Error: '{}' not found in the path '{}'.".format(target_dir, root_path))
        return None
    
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
tests_path = os.path.join(easycut_path, "tests") # easycut-smartbench/tests
asmcnc_path = get_path("asmcnc") # easycut-smartbench/src/asmcnc
skava_ui_img_path = os.path.join(asmcnc_path, "skavaUI", "img") # easycut-smartbench/src/asmcnc/skavaUI/img