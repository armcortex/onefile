import os
import argparse
from datetime import datetime
import tiktoken


def is_supported_file(file_path, supported_extensions):
    return any(file_path.endswith(ext) for ext in supported_extensions)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()


def wrap_in_xml_tags(content, file_name, relative_path):
    tag_name = os.path.join(relative_path, file_name).replace(os.path.sep, '|')
    return f'<{tag_name}>\n{content}\n</{tag_name}>\n\n'


def calculate_token_count(content, encoding_name='cl100k_base'):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(content, allowed_special={'<|endoftext|>'})
    return len(tokens), len(content.split('\n'))


def process_file(file_path, relative_path='', supported_extensions=None, combine=False):
    if not is_supported_file(file_path, supported_extensions):
        return None

    content = read_file(file_path)
    token_count, line_count = calculate_token_count(content)

    print(f'File: {file_path}')
    print(f'Token Count: {token_count}')
    print(f'Line Count: {line_count}')
    print('-' * 50)

    if combine:
        return wrap_in_xml_tags(content, os.path.basename(file_path), relative_path)
    return None


def process_folder(folder_path, skip_folders, supported_extensions, combine=False):
    combined_content = ""
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in skip_folders]
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, folder_path)
            result = process_file(file_path, relative_path, supported_extensions, combine)
            if result:
                combined_content += result
    return combined_content


def main(args):
    supported_extensions = args.supported_extensions or ['.py', '.c', '.cpp', '.h', '.hpp']

    if args.scan_filename:
        process_file(args.scan_filename, supported_extensions=supported_extensions)
    elif args.scan_folder or args.folder_path:
        folder_to_process = args.scan_folder or args.folder_path
        combined_content = process_folder(folder_to_process, args.skip_foldername, supported_extensions, args.combine)

        if args.combine:
            output_folder = args.output_folder or 'result'
            os.makedirs(output_folder, exist_ok=True)
            output_filename = args.output_filename or f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_onefile_result.py'
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(combined_content)

            token_count, line_count = calculate_token_count(combined_content)
            print(f'Output file: {output_path}')
            print(f'Total Token Count: {token_count}')
            print(f'Total Line Count: {line_count}')
    elif args.calc_token:
        content = read_file(args.file_path)
        token_count, line_count = calculate_token_count(content)
        print(f'File: {args.file_path}')
        print(f'Token Count: {token_count}')
        print(f'Line Count: {line_count}')
    else:
        print('Please provide valid arguments. Use -h for help.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and analyze code files.')
    parser.add_argument('--combine', action='store_true', help='Combine supported files into a single output file')
    parser.add_argument('--folder_path', type=str, help='Path to the folder containing supported files')
    parser.add_argument('--calc_token', action='store_true', help='Calculate file token count')
    parser.add_argument('--file_path', type=str, help='File path for token calculation')
    parser.add_argument('--output_folder', type=str, help='Output folder path')
    parser.add_argument('--output_filename', type=str, help='Output filename')
    parser.add_argument('--skip_foldername', nargs='+', default=[], help='List of folder names to skip')
    parser.add_argument('--supported_extensions', nargs='+', help='List of supported file extensions')
    parser.add_argument('--scan_folder', type=str, help='Scan a specific folder and display token counts')
    parser.add_argument('--scan_filename', type=str, help='Scan a specific file and display token count')

    args = parser.parse_args()
    main(args)