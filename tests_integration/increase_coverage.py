import os
import sys


# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from coverage_ai.coverage_ai import CoverAgent


# List of source/test files to iterate over:
SOURCE_TEST_FILE_LIST = [
    # ["coverage_ai/agent_completion_abc.py", "tests/test_agent_completion_abc.py"],
    # ["coverage_ai/ai_caller.py", "tests/test_ai_caller.py"],
    # ["coverage_ai/coverage_ai.py", "tests/test_coverage_ai.py"],
    ["coverage_ai/coverage_processor.py", "tests/test_coverage_processor.py"],
    # ["coverage_ai/custom_logger.py", ""],
    # ["coverage_ai/default_agent_completion.py", "tests/test_default_agent_completion.py"],
    # ["coverage_ai/file_preprocessor.py", "tests/test_file_preprocessor.py"],
    # ["coverage_ai/main.py", "tests/test_main.py"],
    # ["coverage_ai/report_generator.py", "tests/test_report_generator.py"],
    # ["coverage_ai/runner.py", "tests/test_runner.py"],
    # ["coverage_ai/settings/config_loader.py", ""],
    # ["coverage_ai/unit_test_db.py", "tests/test_unit_test_db.py"],
    ["coverage_ai/unit_test_generator.py", "tests/test_unit_test_generator.py"],
    ["coverage_ai/unit_test_validator.py", "tests/test_unit_test_validator.py"],
    # ["coverage_ai/utils.py", "tests/test_load_yaml.py"],
    # ["coverage_ai/version.py", "tests/test_version.py"],
]


class Args:
    def __init__(self, source_file_path, test_file_path):
        self.source_file_path = source_file_path
        self.test_file_path = test_file_path
        self.test_file_output_path = ""
        self.code_coverage_report_path = "coverage.xml"
        self.test_command = "uv run pytest --cov=coverage_ai --cov-report=xml --timeout=30 --disable-warnings"
        self.test_command_dir = os.getcwd()
        self.included_files = None
        self.coverage_type = "cobertura"
        self.report_filepath = "test_results.html"
        self.desired_coverage = 100
        self.max_iterations = 3
        self.additional_instructions = ""
        self.model = "claude-3-7-sonnet-20250219"
        # self.model = "o1-mini"
        self.api_base = "http://localhost:11434"
        self.prompt_only = False
        self.strict_coverage = False
        self.run_tests_multiple_times = 1
        self.use_report_coverage_feature_flag = False
        self.log_db_path = "increase_project_coverage.db"
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.branch = "main"
        self.diff_coverage = False
        self.run_each_test_separately = False
        self.max_run_time_sec = 30


if __name__ == "__main__":
    # Iterate through list of source and test files to run Cover Agent
    for source_file, test_file in SOURCE_TEST_FILE_LIST:
        # Print a banner for the current source file
        banner = f"Testing source file: {source_file}"
        print("\n" + "*" * len(banner))
        print(banner)
        print("*" * len(banner) + "\n")

        args = Args(source_file, test_file)
        agent = CoverAgent(args)
        agent.run()
