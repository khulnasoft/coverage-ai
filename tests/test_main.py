import argparse
import os

from unittest.mock import MagicMock, patch

import pytest

from coverage_ai.main import main, parse_args


@pytest.fixture
def mock_settings():
    """Create a mock settings object with default values."""
    settings = MagicMock()
    settings.get = MagicMock()
    settings.get.side_effect = lambda key: {
        "log_db_path": "logs.db",
        "included_files": None,
        "coverage_type": "cobertura",
        "report_filepath": "test_results.html",
        "desired_coverage": 90,
        "max_iterations": 5,
        "max_run_time_sec": 600,
        "model": "default-model",
        "api_base": "",
        "branch": "develop",
        "strict_coverage": False,
        "run_tests_multiple_times": 1,
        "run_each_test_separately": False,
        "record_mode": False,
        "suppress_log_files": False,
        "use_report_coverage_feature_flag": False,
        "diff_coverage": False,
    }.get(key)
    return settings


@pytest.fixture
def base_args():
    """Create base argument namespace with common values."""
    return argparse.Namespace(
        source_file_path="test_source.py",
        test_file_path="test_file.py",
        project_root="",
        test_file_output_path="",
        code_coverage_report_path="coverage_report.xml",
        test_command="pytest",
        test_command_dir=os.getcwd(),
        included_files=None,
        coverage_type="cobertura",
        report_filepath="test_results.html",
        desired_coverage=90,
        max_iterations=10,
        max_run_time_sec=600,
        additional_instructions="",
        model="gpt-4",
        api_base="",
        strict_coverage=False,
        run_tests_multiple_times=1,
        log_db_path="",
        branch="develop",
        use_report_coverage_feature_flag=False,
        diff_coverage=False,
        run_each_test_separately=False,
        record_mode=False,
        suppress_log_files=True,
    )


class TestMain:
    """Test suite for the main functionalities of the coverage_ai module."""

    @patch("coverage_ai.settings.config_loader.get_settings")
    def test_parse_args(self, mock_get_settings, mock_settings):
        """Test the parse_args function to ensure it correctly parses command-line arguments."""
        mock_get_settings.return_value = {"default": mock_settings}

        with patch(
            "sys.argv",
            [
                "program.py",
                "--source-file-path",
                "test_source.py",
                "--test-file-path",
                "test_file.py",
                "--code-coverage-report-path",
                "coverage_report.xml",
                "--test-command",
                "pytest",
                "--max-iterations",
                "10",
            ],
        ):
            args = parse_args(mock_settings)
            assert args.source_file_path == "test_source.py"
            assert args.test_file_path == "test_file.py"
            assert args.code_coverage_report_path == "coverage_report.xml"
            assert args.test_command == "pytest"
            assert args.test_command_dir == os.getcwd()
            assert args.included_files is None
            assert args.coverage_type == "cobertura"
            assert args.report_filepath == "test_results.html"
            assert args.desired_coverage == 90
            assert args.max_iterations == 10

    @patch("coverage_ai.settings.config_loader.get_settings")
    @patch("coverage_ai.main.CoverAgent")
    def test_main_source_file_not_found(
        self, mock_coverage_ai, mock_get_settings, mock_settings, base_args
    ):
        """Test FileNotFoundError when source file is not found."""
        mock_get_settings.return_value = {"default": mock_settings}

        with patch("coverage_ai.main.parse_args", return_value=base_args):
            mock_agent = MagicMock()
            mock_agent.run.side_effect = FileNotFoundError(
                f"Source file not found at {base_args.source_file_path}"
            )
            mock_coverage_ai.return_value = mock_agent

            with pytest.raises(FileNotFoundError) as exc_info:
                main()

            assert (
                str(exc_info.value)
                == f"Source file not found at {base_args.source_file_path}"
            )

    @patch("coverage_ai.settings.config_loader.get_settings")
    @patch("coverage_ai.main.CoverAgent")
    def test_main_test_file_not_found(
        self, mock_coverage_ai, mock_get_settings, mock_settings, base_args
    ):
        """Test FileNotFoundError when test file is not found."""
        mock_get_settings.return_value = {"default": mock_settings}

        with patch("coverage_ai.main.parse_args", return_value=base_args):
            mock_agent = MagicMock()
            mock_agent.run.side_effect = FileNotFoundError(
                f"Test file not found at {base_args.test_file_path}"
            )
            mock_coverage_ai.return_value = mock_agent

            with pytest.raises(FileNotFoundError) as exc_info:
                main()

            assert (
                str(exc_info.value)
                == f"Test file not found at {base_args.test_file_path}"
            )

    @patch("coverage_ai.settings.config_loader.get_settings")
    @patch("coverage_ai.main.CoverAgent")
    def test_main_calls_agent_run(
        self, mock_coverage_ai, mock_get_settings, mock_settings, base_args
    ):
        """Test that main correctly initializes and runs the CoverAgent."""
        mock_get_settings.return_value = {"default": mock_settings}

        with patch("coverage_ai.main.parse_args", return_value=base_args):
            mock_agent = MagicMock()
            mock_coverage_ai.return_value = mock_agent

            main()

            mock_coverage_ai.assert_called_once()
            mock_agent.run.assert_called_once()

    @patch("coverage_ai.settings.config_loader.get_settings")
    def test_parse_args_with_max_run_time(self, mock_get_settings, mock_settings):
        """Test parsing of max-run-time-sec argument."""
        mock_get_settings.return_value = {"default": mock_settings}

        with patch(
            "sys.argv",
            [
                "program.py",
                "--source-file-path",
                "test_source.py",
                "--test-file-path",
                "test_file.py",
                "--code-coverage-report-path",
                "coverage_report.xml",
                "--test-command",
                "pytest",
                "--max-iterations",
                "10",
                "--max-run-time-sec",
                "45",
            ],
        ):
            args = parse_args(mock_settings)
            assert args.max_run_time_sec == 45
