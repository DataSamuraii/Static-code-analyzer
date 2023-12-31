import os
import re
import sys
import ast

codes_dict = {
    'S001': 'Too long.',
    'S002': 'Indentation is not a multiple of four.',
    'S003': 'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments).',
    'S004': 'Less than two spaces before inline comments.',
    'S005': 'TODO found (in comments only and case-insensitive).',
    'S006': 'More than two blank lines preceding a code line (applies to the first non-empty line).',
    'S007': "Too many spaces after '{}'.",
    'S008': "Class name '{}' should be written in CamelCase.",
    'S009': "Function name '{}' should be written in snake_case.",
    'S010': 'Argument name {} should be written in snake_case.',
    'S011': 'Variable {} should be written in snake_case.',
    'S012': 'The default argument value is mutable.'
}


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.func_args = {}
        self.default_func_args = {}
        self.vars = {}

    def visit_FunctionDef(self, node):
        self.func_args[node.lineno] = [a.arg for a in node.args.args]
        self.default_func_args[node.lineno] = [
            isinstance(a, (ast.List, ast.Dict, ast.Set))
            for a in node.args.defaults
        ]
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.vars[node.lineno] = [
            a.id for a in node.targets if isinstance(a, ast.Name)
        ]
        self.generic_visit(node)

    def get_def_func_args(self):
        return self.default_func_args

    def get_func_args(self):
        return self.func_args

    def get_vars(self):
        return self.vars


def check_line_length(line, line_length):
    if len(line) > line_length:
        return 'S001', None


def check_indentation(line):
    if (len(line) - len(line.lstrip(' '))) % 4 != 0:
        return 'S002', None


def split_line(line):
    code, comment = line.split('#', 1) if '#' in line else (line, '')
    return code, comment


def check_semicolon_and_comments(code, comment):
    if code.strip().endswith(';'):
        return 'S003', None
    if comment and not code.endswith('  ') and code.strip() != '':
        return 'S004', None
    if 'todo' in comment.lower():
        return 'S005', None


def check_blank_lines(blank_line_count):
    if blank_line_count > 2:
        return 'S006', None


def check_keyword_spaces(line):
    keyword_spaces_match = re.search(r'(def|class) {2,}.*', line)
    if keyword_spaces_match:
        keyword = keyword_spaces_match.group(1)
        return 'S007', keyword


def check_naming_conventions(line, line_number, func_args=None, vars_=None, def_func_args=None):
    class_match = re.match(r'class ([a-z]+_?\w+)', line)
    if class_match:
        class_name = class_match.group(1)
        return 'S008', class_name
    f_match = re.search(r'def (__*[A-Z]\w*__|[A-Z]\w*)\b', line)
    if f_match:
        f_name = f_match.group(1)
        return 'S009', f_name
    if line_number in func_args:
        for arg in func_args[line_number]:
            if re.match(r'^(__*[A-Z]\w*__|[A-Z]\w*)\b$', arg):
                return 'S010', arg
    if line_number in vars_:
        for var in vars_[line_number]:
            if re.match(r'^(__*[A-Z]\w*__|[A-Z]\w*)\b$', var):
                return 'S011', var
    if line_number in def_func_args:
        for arg in def_func_args[line_number]:
            if arg:
                return 'S012', arg


def print_errors(file_to_check, line_number, error_code, *args):
    print(f'{file_to_check}: Line {line_number}: {error_code}: {codes_dict[error_code].format(*args)}')


def process_line(file_to_check, line, line_number, analyzer, blank_line_count):
    error_codes_and_args = []
    error_codes_and_args.append(check_line_length(line, 79))
    error_codes_and_args.append(check_indentation(line))

    code, comment = split_line(line)
    error_codes_and_args.append(check_semicolon_and_comments(code, comment))
    error_codes_and_args.append(check_blank_lines(blank_line_count))
    error_codes_and_args.append(check_keyword_spaces(line))
    error_codes_and_args.append(check_naming_conventions(
        line, line_number, analyzer.get_func_args(), analyzer.get_vars(), analyzer.get_def_func_args()))

    for error_code, args in error_codes_and_args:
        if error_code:
            print_errors(file_to_check, line_number, error_code, args)


def process_file(file_to_check):
    with open(file_to_check, 'r', encoding='utf-8') as file_:
        lines = file_.readlines()
        code = ''.join(lines)
        tree = ast.parse(code)
        analyzer = Analyzer()
        analyzer.visit(tree)

        blank_line = 0
        for i, line in enumerate(lines, start=1):
            if not line.strip():
                blank_line += 1
            else:
                blank_line = 0
            process_line(file_to_check, line, i, analyzer, blank_line)


def main():
    sys_args = sys.argv
    folder_path = sys_args[1]
    if folder_path.endswith('.py'):
        process_file(folder_path)
    else:
        folder_content = sorted(os.listdir(folder_path))
        for file in folder_content:
            if file.endswith('.py'):
                full_path = os.path.join(folder_path, file)
                process_file(full_path)


if __name__ == '__main__':
    main()