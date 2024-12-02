# This script retrieves the test results from the unit test database and analyzes them using an LLM

from coverage_ai.UnitTestDB import UnitTestDB
from coverage_ai.AICaller import AICaller

PROMPT_TEMPLATE = """
# Description of Task
You are an assistant that analyzes autogenerated unit tests from an LLM. You are helping a developer to improve the framework of their AI based application and the prompts used to generate the tests.

Your job is to understand why the generated tests failed and provide user feedback on what can be changed in order to make them work. 

Some example ideas to think about:
* Did the user provide enough context to generate the test?
* Where the instructions clear enough to the LLM in the prompt?

DO NOT rewrite the test code. Just explain why the test failed. Try to be as concise as possible.

# Prompt
The following is the prompt we originally used to generate the test suite. It contains the source and test files.
```
{prompt}
```

# Results
The following is the STDOUT of the test:
```
{stdout}
```

The following is the STDERR of the test:
```
{stderr}
```

The follow is the status of the test:
```
{status}
```
"""


def analayze_test_results(
    db_connection_string, response_file_path="test_results_analysis.md"
):
    # Create an instance of the UnitTestDB class
    unit_test_db = UnitTestDB(db_connection_string)

    # Retrieve the test results from the database
    test_results = unit_test_db.get_all_attempts()

    # Analyze the test results using the LLM
    for test_result in test_results:
        # Only analyze failed test results
        if test_result["status"] == "FAIL":
            # Print banner for each test result
            print("============================================================")
            print(f"Test Result ID: {test_result['id']}")
            print("============================================================")

            # Fill in PROMPT string with the test result dictionary contents
            prompt = PROMPT_TEMPLATE.format(
                prompt=test_result["prompt"],
                source_file=test_result["source_file"],
                original_test_file=test_result["original_test_file"],
                processed_test_file=test_result["processed_test_file"],
                stdout=test_result["stdout"],
                stderr=test_result["stderr"],
                status=test_result["status"],
            )

            # Create an instance of the AICaller class
            ai_caller = AICaller(model="gpt-4o")

            # Call the LLM and get the response
            prompt_dict = {"system": "", "user": prompt}
            response, input_token_count, output_token_count = ai_caller.call_model(
                prompt_dict
            )

            # Print the token count of the input and output
            print(f"Input token count: {input_token_count}")
            print(f"Output token count: {output_token_count}")

            # Append the response to a file
            with open(response_file_path, "a") as f:
                f.write(response)


if __name__ == "__main__":
    RESPONSE_FILEPATH = "test_results_analysis.md"

    # Ensure RESPONSE_FILEPATH exists and is empty
    with open(RESPONSE_FILEPATH, "w") as f:
        f.write("")

    db_connection_string = "sqlite:///increase_project_coverage.db"
    analayze_test_results(
        db_connection_string=db_connection_string, response_file_path=RESPONSE_FILEPATH
    )
