import os
import os.path
import glob
import argparse
from datetime import datetime
import tiktoken

def is_supported_file(file_path):
    return file_path.endswith(('.py', '.c', '.cpp', '.h', '.hpp'))


def read_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def wrap_code_in_xml_tags(code, file_name, relative_path):
    if relative_path == '.':
        tag_name = file_name
    else:
        tag_name = os.path.join(relative_path, file_name).replace(os.path.sep, '|')
    return f'<{tag_name}>\n{code}\n</{tag_name}>\n\n'

def calculate_token_count(file_path, encoding_name='cl100k_base'):
    code = read_code(file_path)
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(code, allowed_special={'<|endoftext|>'})
    return len(tokens), len(code.split('\n'))


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
                    relative_path = os.path.relpath(root, folder_location)
                    wrapped_code = wrap_code_in_xml_tags(code, file, relative_path)
                    output_file.write(wrapped_code)
    
    token_cnt, line_cnt = calculate_token_count(output_file_path)
    print(f'Folder path: {output_file_path}')
    print(f'Token Count: {token_cnt}')
    print(f'Line Count: {line_cnt}')

    return output_filename


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process supported files in a folder and generate an "onefile_result.py" file.')
    parser.add_argument('--combine', action='store_true', help='Combine supported files into a single output file')
    parser.add_argument('--folder_path', type=str, help='Path to the folder containing supported files')
    
    parser.add_argument('--calc_token', action='store_true', help='Calculate file token count')
    parser.add_argument('--file_path', type=str, help='File path for token calculation')
    args = parser.parse_args()

    # Process files
    if args.folder_path or args.file_path:
        if args.combine:
            output_filename = process_files(args.folder_path)
            print(f'Processing complete. Check the "{output_filename}" file in the "result" folder.')
            print(f'Folder Path: {args.folder_path}')
        elif args.calc_token:
            token_cnt, line_cnt = calculate_token_count(args.file_path)
            print(f'Folder path: {args.file_path}')
            print(f'Token Count: {token_cnt}')
            print(f'Line Count: {line_cnt}')
    else:
        print('Please provide a folder location using the --path argument.')
