This is the *Static Code Analyzer* project I made myself.
<p>In this project, you will create a simple static analyzer tool that finds common stylistic issues in Python code. You will get a general idea of static code analysis and expand your competence in Python.</p>

Certainly! Below is a simple Markdown documentation that describes the purpose and functionality of this code, outlining the key components.

---
# Python Code Analyzer

The Python Code Analyzer is a static analysis tool designed to identify common coding standards and style issues within Python code files. It leverages both regular expressions and Python's Abstract Syntax Tree (AST) to scan through the code and pinpoint areas where coding conventions may have been violated.

## Features

The analyzer detects the following issues:

- **Line Length**: Checks if any line exceeds 79 characters.
- **Indentation**: Validates that indentation is a multiple of four spaces.
- **Unnecessary Semicolon**: Identifies unnecessary semicolons after statements.
- **Inline Comment Spacing**: Ensures there are at least two spaces before inline comments.
- **TODO Comments**: Detects TODO comments within the code.
- **Blank Lines**: Checks for more than two consecutive blank lines.
- **Keyword Spacing**: Identifies excessive spacing after `def` or `class`.
- **Naming Conventions**: Validates class names are in CamelCase and function names, argument names, and variables are in snake_case.
- **Mutable Default Argument**: Checks for mutable default argument values.

## Usage

The script can be executed directly from the command line by providing a Python file or directory path containing Python files as an argument.

### Example:

```bash
python script_name.py /path/to/directory_or_file
```

## Classes and Functions

### Analyzer

This class utilizes AST to collect data on function arguments, default function arguments, and variables within the code.

### Line and Code Checks

The following functions perform various checks on the code:

- `check_line_length(line, line_length)`: Checks if the line exceeds the specified length.
- `check_indentation(line)`: Validates the indentation of the line.
- `check_semicolon_and_comments(code, comment)`: Checks for unnecessary semicolons and comment spacing.
- `check_blank_lines(blank_line_count)`: Checks for excessive blank lines.
- `check_keyword_spaces(line)`: Checks for excessive spacing after keywords.
- `check_naming_conventions(line, line_number, func_args=None, vars_=None, def_func_args=None)`: Validates naming conventions.

## Extensibility

The code is designed to be easily extensible, allowing for the addition of new checks and modifications to existing ones.

---
Here's the link to the project: https://hyperskill.org/projects/112

Check out my profile: https://hyperskill.org/profile/103100057
