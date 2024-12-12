import os
import pandas as pd

def list_of_Jobs_to_csv(df, file_name="list_of_jobs.csv", folder_name="data"):
    """
    Appends the DataFrame of jobs to a CSV file.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        file_name (str): The name of the CSV file.
        folder_name (str): The folder to store the CSV file.

    Returns:
        None
    """
    try:
        # Create the folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Construct the full file path
        file_path = os.path.join(folder_name, file_name)

        # Append the data to the CSV
        df.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
        print(f"Job list appended to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving the job list to CSV: {e}")


def expanded_skills_to_csv(expanded_df, file_name="expanded_skills.csv", folder_name="data"):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, file_name)

        # Check if the file exists and delete it before appending (optional)
        if not os.path.exists(file_path):
            expanded_df.to_csv(file_path, mode='w', index=False, header=True)
        else:
            expanded_df.to_csv(file_path, mode='a', index=False, header=False)

        print(f"Expanded skills appended to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving the expanded skills to CSV: {e}")

