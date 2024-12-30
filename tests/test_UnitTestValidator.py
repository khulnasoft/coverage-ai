from coverage_ai.CoverageProcessor import CoverageProcessor
from coverage_ai.ReportGenerator import ReportGenerator
from coverage_ai.Runner import Runner
from coverage_ai.UnitTestValidator import UnitTestValidator
from unittest.mock import patch, mock_open
from unittest.mock import MagicMock

import datetime
import os
import pytest
import tempfile


class TestUnitValidator:
    def test_extract_error_message_exception_handling(self):
        # PromptBuilder will not instantiate so we're expecting an empty error_message.
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )
            with patch.object(generator, "ai_caller") as mock_ai_caller:
                mock_ai_caller.call_model.side_effect = Exception("Mock exception")
                fail_details = {
                    "stderr": "stderr content",
                    "stdout": "stdout content",
                    "processed_test_file": "",
                }
                error_message = generator.extract_error_message(fail_details)
                assert "" in error_message

    def test_run_coverage_with_report_coverage_flag(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
                use_report_coverage_feature_flag=True,
            )
            with patch.object(
                Runner, "run_command", return_value=("", "", 0, datetime.datetime.now())
            ):
                with patch.object(
                    CoverageProcessor,
                    "process_coverage_report",
                    return_value={"test.py": ([], [], 1.0)},
                ):
                    generator.run_coverage()
                    # Dividing by zero so we're expecting a logged error and a return of 0
                    assert generator.current_coverage == 0

    def test_extract_error_message_with_prompt_builder(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            # Mock the prompt builder
            mock_prompt_builder = MagicMock()
            generator.prompt_builder = mock_prompt_builder
            mock_prompt_builder.build_prompt_custom.return_value = "test prompt"

            mock_response = """
            error_summary: Test failed due to assertion error in test_example
            """

            with patch.object(
                generator.ai_caller, "call_model", return_value=(mock_response, 10, 10)
            ):
                fail_details = {
                    "stderr": "AssertionError: assert False",
                    "stdout": "test_example failed",
                    "processed_test_file": "",
                }
                error_message = generator.extract_error_message(fail_details)

                assert (
                    error_message
                    == "error_summary: Test failed due to assertion error in test_example"
                )
                mock_prompt_builder.build_prompt_custom.assert_called_once_with(
                    file="analyze_test_run_failure"
                )

    def test_validate_test_pass_no_coverage_increase_with_prompt(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            # Setup initial state
            generator.current_coverage = 0.5
            generator.test_headers_indentation = 4
            generator.relevant_line_number_to_insert_tests_after = 100
            generator.relevant_line_number_to_insert_imports_after = 10
            generator.prompt = {"user": "test prompt"}

            test_to_validate = {
                "test_code": "def test_example(): assert True",
                "new_imports_code": "",
            }

            # Mock file operations
            mock_content = "original content"
            mock_file = mock_open(read_data=mock_content)

            with patch("builtins.open", mock_file), patch.object(
                Runner, "run_command", return_value=("", "", 0, datetime.datetime.now())
            ), patch.object(
                CoverageProcessor, "process_coverage_report", return_value=([], [], 0.4)
            ):

                result = generator.validate_test(test_to_validate)

                assert result["status"] == "FAIL"
                assert result["reason"] == "Coverage did not increase"
                assert result["exit_code"] == 0

    def test_initial_test_suite_analysis_with_prompt_builder(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            # Mock the prompt builder
            mock_prompt_builder = MagicMock()
            generator.prompt_builder = mock_prompt_builder
            mock_prompt_builder.build_prompt_custom.side_effect = [
                "test_headers_indentation: 4",
                "relevant_line_number_to_insert_tests_after: 100\nrelevant_line_number_to_insert_imports_after: 10\ntesting_framework: pytest",
            ]

            # Mock the AI caller responses
            with patch.object(generator.ai_caller, "call_model") as mock_call:
                mock_call.side_effect = [
                    ("test_headers_indentation: 4", 10, 10),
                    (
                        "relevant_line_number_to_insert_tests_after: 100\nrelevant_line_number_to_insert_imports_after: 10\ntesting_framework: pytest",
                        10,
                        10,
                    ),
                ]

                generator.initial_test_suite_analysis()

                assert generator.test_headers_indentation == 4
                assert generator.relevant_line_number_to_insert_tests_after == 100
                assert generator.relevant_line_number_to_insert_imports_after == 10
                assert generator.testing_framework == "pytest"

    def test_post_process_coverage_report_with_report_coverage_flag(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
                use_report_coverage_feature_flag=True,
            )
            with patch.object(
                CoverageProcessor,
                "process_coverage_report",
                return_value={"test.py": ([1], [1], 1.0)},
            ):
                percentage_covered, coverage_percentages = (
                    generator.post_process_coverage_report(datetime.datetime.now())
                )
                assert percentage_covered == 0.5
                assert coverage_percentages == {"test.py": 1.0}

    def test_post_process_coverage_report_with_diff_coverage(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
                diff_coverage=True,
            )
            with patch.object(generator, "generate_diff_coverage_report"), patch.object(
                CoverageProcessor, "process_coverage_report", return_value=([], [], 0.8)
            ):
                percentage_covered, coverage_percentages = (
                    generator.post_process_coverage_report(datetime.datetime.now())
                )
                assert percentage_covered == 0.8

    def test_post_process_coverage_report_without_flags(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )
            with patch.object(
                CoverageProcessor, "process_coverage_report", return_value=([], [], 0.7)
            ):
                percentage_covered, coverage_percentages = (
                    generator.post_process_coverage_report(datetime.datetime.now())
                )
                assert percentage_covered == 0.7

    def test_generate_diff_coverage_report(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            generator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
                diff_coverage=True,
            )
            with patch.object(
                Runner, "run_command", return_value=("", "", 0, datetime.datetime.now())
            ):
                generator.generate_diff_coverage_report()
                assert generator.diff_cover_report_path.endswith(
                    "diff-cover-report.json"
                )

    def test_assess_quality(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            validator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            mock_response = """
            quality: High
            readability: Excellent
            maintainability: Good
            efficiency: High
            """

            with patch.object(
                validator.ai_caller, "call_model", return_value=(mock_response, 10, 10)
            ):
                quality_assessment = validator.assess_quality("generated_code")
                assert quality_assessment["quality"] == "High"
                assert quality_assessment["readability"] == "Excellent"
                assert quality_assessment["maintainability"] == "Good"
                assert quality_assessment["efficiency"] == "High"

    def test_assess_relevance(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            validator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            mock_response = """
            relevance: High
            alignment_with_requirements: Excellent
            appropriateness_of_solution: Good
            """

            with patch.object(
                validator.ai_caller, "call_model", return_value=(mock_response, 10, 10)
            ):
                relevance_assessment = validator.assess_relevance("generated_code")
                assert relevance_assessment["relevance"] == "High"
                assert relevance_assessment["alignment_with_requirements"] == "Excellent"
                assert relevance_assessment["appropriateness_of_solution"] == "Good"

    def test_assess_accuracy(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            validator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            mock_response = """
            accuracy: High
            correctness: Excellent
            adherence_to_specifications: Good
            """

            with patch.object(
                validator.ai_caller, "call_model", return_value=(mock_response, 10, 10)
            ):
                accuracy_assessment = validator.assess_accuracy("generated_code")
                assert accuracy_assessment["accuracy"] == "High"
                assert accuracy_assessment["correctness"] == "Excellent"
                assert accuracy_assessment["adherence_to_specifications"] == "Good"

    def test_log_assessment_results(self):
        with tempfile.NamedTemporaryFile(
            suffix=".py", delete=False
        ) as temp_source_file:
            validator = UnitTestValidator(
                source_file_path=temp_source_file.name,
                test_file_path="test_test.py",
                code_coverage_report_path="coverage.xml",
                test_command="pytest",
                llm_model="gpt-3",
            )

            mock_logger = MagicMock()
            validator.logger = mock_logger

            quality_assessment = {
                "quality": "High",
                "readability": "Excellent",
                "maintainability": "Good",
                "efficiency": "High",
            }
            relevance_assessment = {
                "relevance": "High",
                "alignment_with_requirements": "Excellent",
                "appropriateness_of_solution": "Good",
            }
            accuracy_assessment = {
                "accuracy": "High",
                "correctness": "Excellent",
                "adherence_to_specifications": "Good",
            }

            validator.log_assessment_results(
                quality_assessment, relevance_assessment, accuracy_assessment
            )

            mock_logger.info.assert_any_call(f"Quality Assessment: {quality_assessment}")
            mock_logger.info.assert_any_call(f"Relevance Assessment: {relevance_assessment}")
            mock_logger.info.assert_any_call(f"Accuracy Assessment: {accuracy_assessment}")
