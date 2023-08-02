import os
import re
import sys
import ast

codes_dict = {
    'S001': 'Too long',
    'S002': 'Indentation is not a multiple of four',
    'S003': 'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)',
    'S004': 'Less than two spaces before inline comments',
    'S005': 'TODO found (in comments only and case-insensitive)',
    'S006': 'More than two blank lines preceding a code line (applies to the first non-empty line)',
    'S007': "Too many spaces after '{}'",
    'S008': "Class name '{}' should be written in CamelCase",
    'S009': "Function name '{}' should be written in snake_case",
    'S010': 'Argument name should be written in snake_case',
    'S011': 'Variable should be written in snake_case',
    'S012': 'The default argument value is mutable.'
}


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.func_args = {}
        self.def_func_args = {}
        self.vars = {}

    def visit_FunctionDef(self, node):
        self.func_args[node.lineno] = [a.arg for a in node.args.args]
        self.def_func_args[node.lineno] = [
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
        return self.def_func_args

    def get_func_args(self):
        return self.func_args

    def get_vars(self):
        return self.vars


def return_message(line_idx, message_idx, *args):
    message = codes_dict[message_idx]
    if args:
        message = message.format(*args)
    return f'Line {line_idx}: {message_idx} {message}'


def file_iter(file_to_check):
    with open(file_to_check, 'r', encoding='utf-8') as file_:
        lines = file_.readlines()
        code = ''.join(lines)
        tree = ast.parse(code)

        analyzer = Analyzer()
        analyzer.visit(tree)
        func_args = analyzer.get_func_args()
        def_func_args = analyzer.get_def_func_args()
        vars_ = analyzer.get_vars()

        blank_line = 0
        for i, line in enumerate(lines, start=1):
            error_codes = []

            if len(line) > 79:
                error_codes.append('S001')

            if (len(line) - len(line.lstrip(' '))) % 4 != 0:
                error_codes.append('S002')

            code, comment = line.split('#', 1) if '#' in line else (line, '')

            if code.strip().endswith(';'):
                error_codes.append('S003')

            if comment and not code.endswith('  ') and code.strip() != '':
                error_codes.append('S004')

            if 'todo' in comment.lower():
                error_codes.append('S005')

            if not line.strip():
                blank_line += 1
            else:
                if blank_line > 2:
                    error_codes.append('S006')
                blank_line = 0

            keyword_spaces_match = re.search(r'(def|class) {2}.*', line)
            if keyword_spaces_match:
                keyword = keyword_spaces_match.group(1)
                error_codes.append('S007')

            class_match = re.match(r'class ([a-z]+_?[\w]+)', line)
            if class_match:
                class_name = class_match.group(1)
                error_codes.append('S008')
            f_match = re.search(r'def (__*[A-Z][\w]*__|[A-Z][\w]*)\b', line)
            if f_match:
                f_name = f_match.group(1)
                error_codes.append('S009')

            for code in sorted(set(error_codes)):
                if code == 'S007':
                    print(f'{file_to_check}: {return_message(i, code, keyword)}')
                elif code == 'S008':
                    print(f'{file_to_check}: {return_message(i, code, class_name)}')
                elif code == 'S009':
                    print(f'{file_to_check}: {return_message(i, code, f_name)}')
                else:
                    print(f'{file_to_check}: {return_message(i, code)}')

            if i in func_args:
                for arg in func_args[i]:
                    if re.match(r'^(__*[A-Z][\w]*__|[A-Z][\w]*)\b$', arg):
                        print(f'{file_to_check}: Line {i}: S010: Argument name {arg} should be written in snake_case')
            if i in vars_:
                for var in vars_[i]:
                    if re.match(r'^(__*[A-Z][\w]*__|[A-Z][\w]*)\b$', var):
                        print(f'{file_to_check}: Line {i}: S011: Variable {var} should be written in snake_case')
            if i in def_func_args:
                for arg in def_func_args[i]:
                    if arg:
                        print(f'{file_to_check}: Line {i}: S012: The default argument value is mutable.')


sys_args = sys.argv
folder_path = sys_args[1]

if folder_path.endswith('.py'):
    file_iter(folder_path)
else:
    folder_content = sorted(os.listdir(folder_path))
    for file in folder_content:
        if file.endswith('.py'):
            full_path = os.path.join(folder_path, file)
            file_iter(full_path)
