from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def test_get_files_info(directory):
    print(
        f"Result for {'current' if directory == '.' else f"'{directory}'"} directory:"
    )
    print(get_files_info("calculator", directory))


def test_get_file_contents(file_name):
    print(f"File {file_name} content:")


if __name__ == "__main__":
    # test_get_files_info(".")
    # test_get_files_info("pkg")
    # test_get_files_info("/bin")
    # test_get_files_info("../")
    # print(get_file_content("calculator", "lorem.text"))
    # print(get_file_content("calculator", "main.py"))
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print(get_file_content("calculator", "/bin/cat"))
    # print(get_file_content("calculator", "pkg/does_not_exist.py"))
    # print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
