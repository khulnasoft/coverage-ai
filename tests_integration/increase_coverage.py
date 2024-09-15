import os
import sys

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from coverage_ai.CoverageAi import CoverageAi

# List of source/test files to iterate over:
SOURCE_TEST_FILE_LIST = [
    # ["coverage_ai/AICaller.py", "tests/test_AICaller.py"],
    ["coverage_ai/CoverageAi.py", "tests/test_CoverageAi.py"],
    # ["coverage_ai/CoverageProcessor.py", "tests/test_CoverageProcessor.py"],
    # ["coverage_ai/FilePreprocessor.py", "tests/test_FilePreprocessor.py"],
    # ["coverage_ai/PromptBuilder.py", "tests/test_PromptBuilder.py"],
    # ["coverage_ai/ReportGenerator.py", "tests/test_ReportGenerator.py"],
    # ["coverage_ai/Runner.py", "tests/test_Runner.py"],
    # ["coverage_ai/UnitTestGenerator.py", "tests/test_UnitTestGenerator.py"],
    # ["coverage_ai/version.py", "tests/test_version.py"],
    # ["coverage_ai/utils.py", "tests/test_load_yaml.py"],
    # ["coverage_ai/settings/config_loader.py", "tests/test_.py"],
    # ["coverage_ai/CustomLogger.py",             ""],
]


class Args:
    def __init__(self, source_file_path, test_file_path):
        self.source_file_path = source_file_path
        self.test_file_path = test_file_path
        self.test_file_output_path = ""
        self.code_coverage_report_path = "coverage.xml"
        self.test_command = f"poetry run pytest --cov=coverage_ai --cov-report=xml --cov-report=term --log-cli-level=INFO --timeout=30"
        self.test_command_dir = os.getcwd()
        self.included_files = None
        self.coverage_type = "cobertura"
        self.report_filepath = "test_results.html"
        self.desired_coverage = 100
        self.max_iterations = 5
        self.additional_instructions = "Use as much mocking as possible"
        self.model = "gpt-4o"
        self.api_base = "http://localhost:11434"
        self.prompt_only = False
        self.strict_coverage = False


if __name__ == "__main__":
    # Iterate through list of source and test files to run Coverage Ai
    for source_file, test_file in SOURCE_TEST_FILE_LIST:
        # Print a banner for the current source file
        banner = f"Testing source file: {source_file}"
        print("\n" + "*" * len(banner))
        print(banner)
        print("*" * len(banner) + "\n")

        args = Args(source_file, test_file)
        agent = CoverageAi(args)
        agent.run()
