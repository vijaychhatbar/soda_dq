import subprocess
import os
import sys
from google.cloud import logging as gcp_logging

#set up Google Cloud Logging
client = gcp_logging.Client()
logger = client.logger("soda-dq")  # Replace with your actual logger name

# Define the path to the /checks directory
checks_directory = "/checks"

# List all .yml files in the /checks directory
yml_files = [os.path.join(checks_directory, filename) for filename in os.listdir(checks_directory) if filename.endswith('.yml')]
return_code = []
try:
    for yml_file in yml_files:
        # Define the Docker command for each .yml file
        docker_command = f"soda scan -d demo -c configuration.yml {yml_file}"
        
        # Execute the Docker command and capture the output
        result = subprocess.run(docker_command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return_code_list = return_code.append(result.returncode)
        if result.returncode != 0:
            print(f"Error executing command for {yml_file}. Return code: {result.returncode}")
            print("Actual Error output:\n", result.stdout)
                # Log error to Google Cloud Logging
            logger.log_struct(
                    {
                        "severity": "ERROR",
                        "message": f"Error executing command for {yml_file}. Return code: {result.returncode}",
                        "output": result.stdout,
                    }
            )
        else:
            print(f"Command for {yml_file} executed successfully!")
            print("Output:\n", result.stdout)
            # Log success to Google Cloud Logging
            logger.log_struct(
                    {
                        "severity": "INFO",
                        "message": f"Command for {yml_file} executed successfully",
                        "output": result.stdout,
                    }
            )


except subprocess.CalledProcessError as e:
    print("CalledProcessError:", e)
        # Log error to Google Cloud Logging
    logger.log_struct(
        {
            "severity": "ERROR",
            "message": f"Error executing command.",
            "error": e,
        }
    )

# Check if any of the return codes are not equal to 0
if any(code != 0 for code in return_code):
    sys.exit(1)  # Exit with a non-zero status code to indicate failure

