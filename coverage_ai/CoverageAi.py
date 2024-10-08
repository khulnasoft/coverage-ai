import datetime
import os
import shutil
import sys
import wandb

from coverage_ai.CustomLogger import CustomLogger
from coverage_ai.ReportGenerator import ReportGenerator
from coverage_ai.UnitTestGenerator import UnitTestGenerator
from coverage_ai.UnitTestDB import UnitTestDB


class CoverageAi:
    def __init__(self, args):
        self.args = args
        self.logger = CustomLogger.get_logger(__name__)

        self._validate_paths()
        self._duplicate_test_file()

        self.test_gen = UnitTestGenerator(
            source_file_path=args.source_file_path,
            test_file_path=args.test_file_output_path,
            code_coverage_report_path=args.code_coverage_report_path,
            test_command=args.test_command,
            test_command_dir=args.test_command_dir,
            included_files=args.included_files,
            coverage_type=args.coverage_type,
            desired_coverage=args.desired_coverage,
            additional_instructions=args.additional_instructions,
            llm_model=args.model,
            api_base=args.api_base,
            use_report_coverage_feature_flag=args.use_report_coverage_feature_flag,
        )

    def _validate_paths(self):
        if not os.path.isfile(self.args.source_file_path):
            raise FileNotFoundError(
                f"Source file not found at {self.args.source_file_path}"
            )
        if not os.path.isfile(self.args.test_file_path):
            raise FileNotFoundError(
                f"Test file not found at {self.args.test_file_path}"
            )
        if not self.args.log_db_path:
            # Create default DB file if not provided
            self.args.log_db_path = "coverage_ai_unit_test_runs.db"
        self.test_db = UnitTestDB(
            db_connection_string=f"sqlite:///{self.args.log_db_path}"
        )

    def _duplicate_test_file(self):
        if self.args.test_file_output_path != "":
            shutil.copy(self.args.test_file_path, self.args.test_file_output_path)
        else:
            self.args.test_file_output_path = self.args.test_file_path

    def run(self):
        if "WANDB_API_KEY" in os.environ:
            wandb.login(key=os.environ["WANDB_API_KEY"])
            time_and_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            run_name = f"{self.args.model}_" + time_and_date
            wandb.init(project="coverage-ai", name=run_name)

        iteration_count = 0
        test_results_list = []

        self.test_gen.initial_test_suite_analysis()

        while (
            self.test_gen.current_coverage < (self.test_gen.desired_coverage / 100)
            and iteration_count < self.args.max_iterations
        ):
            self.logger.info(
                f"Current Coverage: {round(self.test_gen.current_coverage * 100, 2)}%"
            )
            self.logger.info(f"Desired Coverage: {self.test_gen.desired_coverage}%")

            generated_tests_dict = self.test_gen.generate_tests(max_tokens=4096)

            for generated_test in generated_tests_dict.get("new_tests", []):
                test_result = self.test_gen.validate_test(
                    generated_test, self.args.run_tests_multiple_times
                )
                test_results_list.append(test_result)

                # Insert the test result into the database
                self.test_db.insert_attempt(test_result)

            iteration_count += 1

            if self.test_gen.current_coverage < (self.test_gen.desired_coverage / 100):
                self.test_gen.run_coverage()

        if self.test_gen.current_coverage >= (self.test_gen.desired_coverage / 100):
            self.logger.info(
                f"Reached above target coverage of {self.test_gen.desired_coverage}% (Current Coverage: {round(self.test_gen.current_coverage * 100, 2)}%) in {iteration_count} iterations."
            )
        elif iteration_count == self.args.max_iterations:
            failure_message = f"Reached maximum iteration limit without achieving desired coverage. Current Coverage: {round(self.test_gen.current_coverage * 100, 2)}%"
            if self.args.strict_coverage:
                # User requested strict coverage (similar to "--cov-fail-under in pytest-cov"). Fail with exist code 2.
                self.logger.error(failure_message)
                sys.exit(2)
            else:
                self.logger.info(failure_message)

        # Provide metric on total token usage
        self.logger.info(
            f"Total number of input tokens used for LLM model {self.test_gen.ai_caller.model}: {self.test_gen.total_input_token_count}"
        )
        self.logger.info(
            f"Total number of output tokens used for LLM model {self.test_gen.ai_caller.model}: {self.test_gen.total_output_token_count}"
        )

        ReportGenerator.generate_report(test_results_list, self.args.report_filepath)

        if "WANDB_API_KEY" in os.environ:
            wandb.finish()
