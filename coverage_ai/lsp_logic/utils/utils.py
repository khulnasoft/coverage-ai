import itertools
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import unquote, urlparse

# import git

# from coverage_ai.lsp_logic.utils import io

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}


def find_relevant_files_in_repo(repo_root: str, chat_files: list[str]):
    gitignore_file = Path(repo_root) / ".gitignore"
    gitignore_content = ""
    if (gitignore_file.exists()):
        with open(gitignore_file, "r") as f:
            gitignore_content = f.read().strip().split("\n")

    # get all files in the repo
    repo_files = []
    chat_file_type = chat_files[0].split(".")[-1]
    root = repo_root
    for root, dirs, files in os.walk(root):
        for file in files:
            file_type = file.split(".")[-1]
            if (file_type != chat_file_type):
                continue
            # gitignore_content
            relative_path = os.path.relpath(os.path.join(root, file), repo_root)
            if (gitignore_content):
                if (any(relative_path.startswith(pattern) for pattern in gitignore_content)):
                    continue
            if ('venv/' in relative_path):
                continue

            repo_files.append(os.path.join(root, file))
    return repo_files

class IgnorantTemporaryDirectory:
    def __init__(self):
        if (sys.version_info >= (3, 10)):
            self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        else:
            self.temp_dir = tempfile.TemporaryDirectory()

    def __enter__(self):
        return self.temp_dir.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        try:
            self.temp_dir.cleanup()
        except (OSError, PermissionError, RecursionError):
            pass  # Ignore errors (Windows and potential recursion)

    def __getattr__(self, item):
        return getattr(self.temp_dir, item)


class ChdirTemporaryDirectory(IgnorantTemporaryDirectory):
    def __init__(self):
        try:
            self.cwd = os.getcwd()
        except FileNotFoundError:
            self.cwd = None

        super().__init__()

    def __enter__(self):
        res = super().__enter__()
        os.chdir(Path(self.temp_dir.name).resolve())
        return res

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.cwd):
            try:
                os.chdir(self.cwd)
            except FileNotFoundError:
                pass
        super().__exit__(exc_type, exc_val, exc_tb)


# class GitTemporaryDirectory(ChdirTemporaryDirectory):
#     def __enter__(self):
#         dname = super().__enter__()
#         self.repo = make_repo(dname)
#         return dname
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         del self.repo
#         super().__exit__(exc_type, exc_val, exc_tb)
#
#
# def make_repo(path=None):
#     if not path:
#         path = "."
#     repo = git.Repo.init(path)
#     repo.config_writer().set_value("user", "name", "Test User").release()
#     repo.config_writer().set_value("user", "email", "testuser@example.com").release()
#
#     return repo


def is_image_file(file_name):
    """
    Check if the given file name has an image file extension.

    :param file_name: The name of the file to check.
    :return: True if the file is an image, False otherwise.
    """
    file_name = str(file_name)  # Convert file_name to string
    return any(file_name.endswith(ext) for ext in IMAGE_EXTENSIONS)


def safe_abs_path(res):
    "Gives an abs path, which safely returns a full (not 8.3) windows path"
    res = Path(res).resolve()
    return str(res)


def format_content(role, content):
    formatted_lines = []
    for line in content.splitlines():
        formatted_lines.append(f"{role} {line}")
    return "\n".join(formatted_lines)


def format_messages(messages, title=None):
    output = []
    if (title):
        output.append(f"{title.upper()} {'*' * 50}")

    for msg in messages:
        output.append("")
        role = msg["role"].upper()
        content = msg.get("content")
        if (isinstance(content, list)):  # Handle list content (e.g., image messages)
            for item in content:
                if (isinstance(item, dict)):
                    for key, value in item.items():
                        if (isinstance(value, dict) and "url" in value):
                            output.append(f"{role} {key.capitalize()} URL: {value['url']}")
                        else:
                            output.append(f"{role} {key}: {value}")
                else:
                    output.append(f"{role} {item}")
        elif (isinstance(content, str)):  # Handle string content
            output.append(format_content(role, content))
        function_call = msg.get("function_call")
        if (function_call):
            output.append(f"{role} Function Call: {function_call}")

    return "\n".join(output)


def show_messages(messages, title=None, functions=None):
    formatted_output = format_messages(messages, title)
    print(formatted_output)

    # if functions:
    #     dump(functions)


def split_chat_history_markdown(text, include_tool=False):
    messages = []
    user = []
    assistant = []
    tool = []
    lines = text.splitlines(keepends=True)

    def append_msg(role, lines):
        lines = "".join(lines)
        if (lines.strip()):
            messages.append(dict(role=role, content=lines))

    for line in lines:
        if (line.startswith("# ")):
            continue
        if (line.startswith("> ")):
            append_msg("assistant", assistant)
            assistant = []
            append_msg("user", user)
            user = []
            tool.append(line[2:])
            continue
        # if line.startswith("#### /"):
        #    continue

        if (line.startswith("#### ")):
            append_msg("assistant", assistant)
            assistant = []
            append_msg("tool", tool)
            tool = []

            content = line[5:]
            user.append(content)
            continue

        append_msg("user", user)
        user = []
        append_msg("tool", tool)
        tool = []

        assistant.append(line)

    append_msg("assistant", assistant)
    append_msg("user", user)

    if (not include_tool):
        messages = [m for m in messages if (m["role"] != "tool")]

    return messages


# Copied from pip, MIT license
# https://github.com/pypa/pip/blob/b989e6ef04810bbd4033a3683020bd4ddcbdb627/src/pip/_internal/utils/entrypoints.py#L73
def get_best_invocation_for_this_python() -> str:
    """Try to figure out the best way to invoke the current Python."""
    exe = sys.executable
    exe_name = os.path.basename(exe)

    # Try to use the basename, if it's the first executable.
    found_executable = shutil.which(exe_name)
    if (found_executable and os.path.samefile(found_executable, exe)):
        return exe_name

    # Use the full executable name, because we couldn't find something simpler.
    return exe


def get_pip_install(args):
    cmd = [
        get_best_invocation_for_this_python(),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--upgrade-strategy",
        "only-if-needed",
    ]
    cmd += args
    return cmd


def run_install(cmd):
    print()
    print("Installing:", printable_shell_command(cmd))

    try:
        output = []
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding=sys.stdout.encoding,
            errors="replace",
        )
        spinner = Spinner("Installing...")

        while True:
            char = process.stdout.read(1)
            if (not char):
                break

            output.append(char)
            spinner.step()

        spinner.end()
        return_code = process.wait()
        output = "".join(output)

        if (return_code == 0):
            print("Installation complete.")
            print()
            return True, output

    except subprocess.CalledProcessError as e:
        print(f"\nError running pip install: {e}")

    print("\nInstallation failed.\n")

    return False, output


class Spinner:
    spinner_chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    def __init__(self, text):
        self.text = text
        self.start_time = time.time()
        self.last_update = 0
        self.visible = False

    def step(self):
        current_time = time.time()
        if (not self.visible and current_time - self.start_time >= 0.5):
            self.visible = True
            self._step()
        elif (self.visible and current_time - self.last_update >= 0.1):
            self._step()
        self.last_update = current_time

    def _step(self):
        if (not self.visible):
            return

        print(f"\r{self.text} {next(self.spinner_chars)}\r{self.text} ", end="", flush=True)

    def end(self):
        if (self.visible):
            print("\r" + " " * (len(self.text) + 3))


def find_common_root(abs_fnames):
    if (len(abs_fnames) == 1):
        return safe_abs_path(os.path.dirname(list(abs_fnames)[0]))
    elif (abs_fnames):
        return safe_abs_path(os.path.commonpath(list(abs_fnames)))
    else:
        return safe_abs_path(os.getcwd())


def format_tokens(count):
    if (count < 1000):
        return f"{count}"
    elif (count < 10000):
        return f"{count / 1000:.1f}k"
    else:
        return f"{round(count / 1000)}k"


def touch_file(fname):
    fname = Path(fname)
    try:
        fname.parent.mkdir(parents=True, exist_ok=True)
        fname.touch()
        return True
    except OSError:
        return False


def check_pip_install_extra(io, module, prompt, pip_install_cmd, self_update=False):
    if (module):
        try:
            __import__(module)
            return True
        except (ImportError, ModuleNotFoundError, RuntimeError):
            pass

    cmd = get_pip_install(pip_install_cmd)

    if (prompt):
        io.tool_warning(prompt)

    if (self_update and platform.system() == "Windows"):
        io.tool_output("Run this command to update:")
        print()
        print(printable_shell_command(cmd))  # plain print so it doesn't line-wrap
        return

    if (not io.confirm_ask("Run pip install?", default="y", subject=printable_shell_command(cmd))):
        return

    success, output = run_install(cmd)
    if (success):
        if (not module):
            return True
        try:
            __import__(module)
            return True
        except (ImportError, ModuleNotFoundError, RuntimeError) as err:
            io.tool_error(str(err))
            pass

    io.tool_error(output)

    print()
    print("Install failed, try running this command manually:")
    print(printable_shell_command(cmd))


def printable_shell_command(cmd_list):
    """
    Convert a list of command arguments to a properly shell-escaped string.

    Args:
        cmd_list (list): List of command arguments.

    Returns:
        str: Shell-escaped command string.
    """
    if (platform.system() == "Windows"):
        return subprocess.list2cmdline(cmd_list)
    else:
        return shlex.join(cmd_list)


def uri_to_path(uri):
    return unquote(urlparse(uri).path)


def is_forbidden_directory(d_path, language):
    directories_to_ignore = []
    if (language == 'python'):
        directories_to_ignore = [
            'venv',  # Virtual environment
            'pyenv',  # Python environment
            '__pycache__/',  # Compiled Python files
            'dist/',  # Distribution directories
            'build/',  # Build directories
        ]
    elif (language == 'javascript' or language == 'typescript'):
        directories_to_ignore = [
            'node_modules/',  # Dependencies installed by npm or yarn
            'dist/',  # Common output directory for built files
            'build/',  # Another common output directory for built files
            'coverage/',  # Test coverage reports
            '.cache/',  # Cache directory (used by some build tools)
            '.next/',  # Next.js build output
            '.nuxt/',  # Nuxt.js build output
            '.DS_Store'  # macOS folder attributes
        ]
    elif (language == 'java'):
        directories_to_ignore = [
            'target/',  # Maven build directory
            'build/',  # Gradle build directory
            '.gradle/',  # Gradle-specific files and caches
            '.idea/',  # IntelliJ IDEA settings
            '.iml',  # IntelliJ IDEA module files
            '.classpath',  # Eclipse project file
            '.project',  # Eclipse project file
            'out/'  # Output directory for IntelliJ IDEA
        ]
    elif (language == 'rust'):
        directories_to_ignore = [
            'target/',  # Default output directory for compiled artifacts
            'Cargo.lock',  # Lock file for cargo dependencies (ignored for libraries, kept for binaries)
            '.cargo/',  # Cargo cache directory
        ]
    elif (language == 'csharp'):
        directories_to_ignore = [
            'bin/',  # Output directory for compiled binaries
            'obj/',  # Intermediate output directory for object files
            '.vs/',  # Visual Studio specific files
            '.vscode/',  # Visual Studio Code specific files
            'packages/',  # NuGet packages directory
            'TestResults/',  # Test results directory
        ]
    elif (language == 'go'):
        directories_to_ignore = [
            'bin/',  # Output directory for compiled binaries
            'pkg/',  # Package object files directory
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'vendor/',  # Vendor directory for dependencies
        ]
    elif (language == 'ruby'):
        directories_to_ignore = [
            '.bundle/',  # Bundler specific files
            'vendor/bundle/',  # Vendor directory for bundled gems
            '.yardoc/',  # YARD documentation files
            '_yardoc/',  # YARD documentation files
            'coverage/',  # Test coverage reports
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'php'):
        directories_to_ignore = [
            'vendor/',  # Vendor directory for dependencies
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'elixir'):
        directories_to_ignore = [
            '_build/',  # Build artifacts directory
            'deps/',  # Dependencies directory
            '.elixir_ls/',  # Elixir Language Server specific files
            'cover/',  # Test coverage reports
        ]
    elif (language == 'swift'):
        directories_to_ignore = [
            '.build/',  # Build artifacts directory
            'Packages/',  # Swift package manager dependencies
            '.swiftpm/',  # Swift package manager specific files
            '.xcodeproj/',  # Xcode project files
            '.xcworkspace/',  # Xcode workspace files
        ]
    elif (language == 'kotlin'):
        directories_to_ignore = [
            'build/',  # Build directory
            '.gradle/',  # Gradle-specific files and caches
            '.idea/',  # IntelliJ IDEA settings
            '.iml',  # IntelliJ IDEA module files
            '.classpath',  # Eclipse project file
            '.project',  # Eclipse project file
            'out/'  # Output directory for IntelliJ IDEA
        ]
    elif (language == 'scala'):
        directories_to_ignore = [
            'target/',  # Build directory
            'project/target/',  # SBT build directory
            'project/project/',  # SBT project directory
            '.idea/',  # IntelliJ IDEA settings
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'perl'):
        directories_to_ignore = [
            'blib/',  # Build directory
            '_build/',  # Build directory
            '.build/',  # Build directory
            'Build/',  # Build directory
            'Build.bat',  # Build script
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'r'):
        directories_to_ignore = [
            '.Rproj.user/',  # RStudio project files
            '.Rhistory/',  # R history files
            '.RData/',  # R data files
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'haskell'):
        directories_to_ignore = [
            'dist/',  # Build directory
            'dist-newstyle/',  # Build directory
            '.stack-work/',  # Stack build directory
            '.cabal-sandbox/',  # Cabal sandbox directory
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'lua'):
        directories_to_ignore = [
            '.luarocks/',  # LuaRocks specific files
            'deps/',  # Dependencies directory
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'shell'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'powershell'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'dart'):
        directories_to_ignore = [
            '.dart_tool/',  # Dart tool specific files
            'build/',  # Build directory
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'clojure'):
        directories_to_ignore = [
            'target/',  # Build directory
            '.cpcache/',  # Clojure CLI tool cache
            '.lein-repl-history',  # Leiningen REPL history
            '.nrepl-port',  # nREPL port file
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'groovy'):
        directories_to_ignore = [
            'build/',  # Build directory
            '.gradle/',  # Gradle-specific files and caches
            '.idea/',  # IntelliJ IDEA settings
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'julia'):
        directories_to_ignore = [
            '.julia/',  # Julia package directory
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
        ]
    elif (language == 'matlab'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'objective-c'):
        directories_to_ignore = [
            'build/',  # Build directory
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
        ]
    elif (language == 'ocaml'):
        directories_to_ignore = [
            '_build/',  # Build directory
            '.merlin/',  # Merlin specific files
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'racket'):
        directories_to_ignore = [
            '.racket/',  # Racket specific files
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'rust'):
        directories_to_ignore = [
            'target/',  # Default output directory for compiled artifacts
            'Cargo.lock',  # Lock file for cargo dependencies (ignored for libraries, kept for binaries)
            '.cargo/',  # Cargo cache directory
        ]
    elif (language == 'scala'):
        directories_to_ignore = [
            'target/',  # Build directory
            'project/target/',  # SBT build directory
            'project/project/',  # SBT project directory
            '.idea/',  # IntelliJ IDEA settings
            '.vscode/',  # Visual Studio Code specific files
        ]
    elif (language == 'smalltalk'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'sql'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'tcl'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'vbnet'):
        directories_to_ignore = [
            'bin/',  # Output directory for compiled binaries
            'obj/',  # Intermediate output directory for object files
            '.vs/',  # Visual Studio specific files
            '.vscode/',  # Visual Studio Code specific files
            'packages/',  # NuGet packages directory
            'TestResults/',  # Test results directory
        ]
    elif (language == 'verilog'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'vhdl'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'xml'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'yaml'):
        directories_to_ignore = [
            '.vscode/',  # Visual Studio Code specific files
            '.idea/',  # IntelliJ IDEA settings
            'node_modules/',  # Dependencies installed by npm or yarn
        ]
    elif (language == 'zig'):
        directories_to_ignore = [
            'zig-cache/',  # Zig cache directory
            'zig-out/',  # Zig output directory
            '.vscode/',  # Visual Studio Code specific files
        ]
    if (any([directory in d_path for directory in directories_to_ignore])):
        return True

    return False
