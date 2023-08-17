import shutil
import sys
import os
import re

class helpers:

    def setup_folder(path):
        """
        Restart folder (delete it and create it)
        """
        try:
            if os.path.exists(path):
                # Delete all contents of the existing directory
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")
            else:
                # Create the directory
                # This function also creates all the necessary intermediate directories if they don't exist
                os.makedirs(path)     
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        
    
    def check_if_empty(input: any, input_name: str):
        """
        Raise an exception if input string is empty
        """
        try:
            if not input: raise Exception(f"The {input_name} input is empty")        
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        

    def remove_special_characters(input_string: str):
        """
        Removes the special characters from an input string
        """
        try:
            return re.sub(r'[^a-zA-Z0-9 ]+', '', input_string)[:60]
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        
    
    def count_substring(sub_text: str, main_text: any):
        """
        Returns the number of phrase occurrences
        """
        try:
            return main_text.lower().count(sub_text.lower())
        except Exception as err:
            exc_tb = sys.exc_info()[2]
            raise Exception(f'{err} ({exc_tb.tb_lineno})')
        
