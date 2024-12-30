import subprocess
import time

from coverage_ai.settings.config_loader import get_settings


class Runner:
    @staticmethod
    def run_command(command, cwd=None):
        """
        Executes a shell command in a specified working directory and returns its output, error, and exit code.

        Parameters:
            command (str): The shell command to execute.
            cwd (str, optional): The working directory in which to execute the command. Defaults to None.

        Returns:
            tuple: A tuple containing the standard output ('stdout'), standard error ('stderr'), exit code ('exit_code'), and the time of the executed command ('command_start_time').
        """
        # Get the current time before running the test command, in milliseconds
        command_start_time = int(round(time.time() * 1000))

        max_allowed_runtime_seconds = get_settings().get(
            "tests.max_allowed_runtime_seconds", 30
        )
        # Ensure the command is executed with shell=True for string commands
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                text=True,
                capture_output=True,
                timeout=max_allowed_runtime_seconds,
            )

            # Return a dictionary with the desired information
            return result.stdout, result.stderr, result.returncode, command_start_time
        except subprocess.TimeoutExpired:
            # Handle the timeout case
            return "", "Command timed out", -1, command_start_time

    @staticmethod
    def assess_quality_relevance_accuracy(stdout, stderr):
        """
        Assess the quality, relevance, and accuracy of the command output.

        Parameters:
            stdout (str): The standard output of the command.
            stderr (str): The standard error of the command.

        Returns:
            dict: A dictionary containing the quality, relevance, and accuracy assessments.
        """
        quality_assessment = Runner.assess_quality(stdout, stderr)
        relevance_assessment = Runner.assess_relevance(stdout, stderr)
        accuracy_assessment = Runner.assess_accuracy(stdout, stderr)

        return {
            "quality": quality_assessment,
            "relevance": relevance_assessment,
            "accuracy": accuracy_assessment,
        }

    @staticmethod
    def assess_quality(stdout, stderr):
        """
        Assess the quality of the command output.

        Parameters:
            stdout (str): The standard output of the command.
            stderr (str): The standard error of the command.

        Returns:
            dict: A dictionary containing the quality assessment results.
        """
        # Placeholder implementation, replace with actual assessment logic
        return {"quality": "assessed"}

    @staticmethod
    def assess_relevance(stdout, stderr):
        """
        Assess the relevance of the command output.

        Parameters:
            stdout (str): The standard output of the command.
            stderr (str): The standard error of the command.

        Returns:
            dict: A dictionary containing the relevance assessment results.
        """
        # Placeholder implementation, replace with actual assessment logic
        return {"relevance": "assessed"}

    @staticmethod
    def assess_accuracy(stdout, stderr):
        """
        Assess the accuracy of the command output.

        Parameters:
            stdout (str): The standard output of the command.
            stderr (str): The standard error of the command.

        Returns:
            dict: A dictionary containing the accuracy assessment results.
        """
        # Placeholder implementation, replace with actual assessment logic
        return {"accuracy": "assessed"}
