import os
import re
import concurrent.futures

def find_imports_in_file(file_path):
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            imports = re.findall(r'^\s*(?:import|from)\s+(\S+)', content, re.MULTILINE)
            return set(imports)
        except UnicodeDecodeError:
            continue
    print(f"Failed to decode {file_path} with available encodings.")
    return set()

def find_all_imports(project_dir):
    all_imports = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    futures.append(executor.submit(find_imports_in_file, file_path))
        
        for future in concurrent.futures.as_completed(futures):
            all_imports.update(future.result())
    return all_imports

def filter_standard_library(imports):
    import sys
    std_libs = set(sys.stdlib_module_names)
    return [imp for imp in imports if imp not in std_libs and not imp.startswith('.')]

def write_requirements_txt(imports, output_file='requirements.txt'):
    with open(output_file, 'w') as file:
        for imp in sorted(imports):
            file.write(f"{imp}\n")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_requirements.py <project_directory>")
        sys.exit(1)

    project_directory = sys.argv[1]
    all_imports = find_all_imports(project_directory)
    filtered_imports = filter_standard_library(all_imports)
    write_requirements_txt(filtered_imports)
    print(f"requirements.txt generated with {len(filtered_imports)} packages.")
