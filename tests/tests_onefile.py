import os
import pytest
from onefile.onefile import is_supported_file, read_code, wrap_code_in_xml_tags, process_files


@pytest.fixture
def setup_files(tmp_path):
    # Create a temporary directory and sample files for testing
    file1 = tmp_path / 'file1.py'
    file1.write_text('print("Hello from file1")')

    file2 = tmp_path / 'file2.c'
    file2.write_text('#include <stdio.h>\nint main() { printf("Hello from file2"); return 0; }')

    file3 = tmp_path / 'file3.cpp'
    file3.write_text('#include <iostream>\nint main() { std::cout << "Hello from file3"; return 0; }')

    file4 = tmp_path / 'file4.txt'
    file4.write_text('This is not a supported file')

    return tmp_path


@pytest.mark.parametrize('file_path, expected_result', [
    ('file1.py', True),
    ('file2.c', True),
    ('file3.cpp', True),
    ('file4.txt', False)
])
def test_is_supported_file(file_path, expected_result):
    assert is_supported_file(file_path) == expected_result


def test_read_code(setup_files):
    file_path = setup_files / 'file1.py'
    expected_code = 'print("Hello from file1")'
    assert read_code(file_path) == expected_code


def test_wrap_code_in_xml_tags():
    code = 'print("Hello")'
    file_name = 'example.py'
    expected_output = '<example.py>\nprint("Hello")\n</example.py>\n\n'
    assert wrap_code_in_xml_tags(code, file_name) == expected_output


def test_process_files_recursive(setup_files):
    output_filename = process_files(setup_files)
    output_file_path = f'result/{output_filename}'

    assert os.path.exists(output_file_path)

    with open(output_file_path, 'r') as file:
        content = file.read()
        assert '<file1.py>\nprint("Hello from file1")\n</file1.py>' in content
        assert '<file2.c>\n#include <stdio.h>\nint main() { printf("Hello from file2"); return 0; }\n</file2.c>' in content
        assert '<file3.cpp>\n#include <iostream>\nint main() { std::cout << "Hello from file3"; return 0; }\n</file3.cpp>' in content
        assert 'file4.txt' not in content

    os.remove(output_file_path)  # Clean up the generated onefile_result.txt file