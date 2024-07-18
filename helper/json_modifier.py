import os
import shutil

def replace_json_file(file_path, new_file_path):
    try:
        # Remove the old file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Copy the new file to the original file path
        shutil.copyfile(new_file_path, file_path)
        
        return True, "JSON file updated successfully"
    except Exception as e:
        return False, f"Error updating JSON file: {str(e)}"



