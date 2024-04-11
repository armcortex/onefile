import os
import os.path
import glob
import argparse
from datetime import datetime


def is_supported_file(file_path):
    return file_path.endswith(('.py', '.c', '.cpp'))


def read_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def wrap_code_in_xml_tags(code, file_name):
    return f'<{file_name}>\n{code}\n</{file_name}>\n\n'


def process_files(folder_location):
    result_folder = 'result'
    os.makedirs(result_folder, exist_ok=True)

    output_filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_onefile_result.py'
    output_file_path = os.path.join(result_folder, output_filename)
    with open(output_file_path, 'w') as output_file:
        for root, dirs, files in os.walk(folder_location):
            for file in files:
                file_path = os.path.join(root, file)
                if is_supported_file(file_path):
                    code = read_code(file_path)
                    wrapped_code = wrap_code_in_xml_tags(code, file)
                    output_file.write(wrapped_code)

    return output_filename


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process supported files in a folder and generate an "onefile_result.py" file.')
    parser.add_argument('--path', type=str, help='Path to the folder containing supported files')
    args = parser.parse_args()

    # Process files
    folder_location = args.path
    if folder_location:
        output_filename = process_files(folder_location)
        print(f'Processing complete. Check the "{output_filename}" file in the "result" folder.')
        print(f'Path: {folder_location}')
    else:
        print('Please provide a folder location using the --path argument.')
