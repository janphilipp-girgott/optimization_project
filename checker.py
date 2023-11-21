import pandas as pd
import os
from datetime import timedelta
from multiprocessing import Pool

def check_date_range(file_path):
    try:
        # Read the first row of the file
        first_row = pd.read_csv(file_path, nrows=1)

        # If the file is empty or has only one row
        if first_row.empty:
            print(f"File {file_path} is empty.")
            return False  # Not enough data to calculate a date range

        # Read the last row - we'll use the chunksize approach again
        with pd.read_csv(file_path, chunksize=1) as reader:
            last_row = None
            for row in reader:
                last_row = row

        if last_row is None:
            print(f"File {file_path} does not have enough data.")
            return False

        # Extract dates from the first and last row
        first_date = pd.to_datetime(first_row['Date'].iloc[0])
        last_date = pd.to_datetime(last_row['Date'].iloc[0])

        # Calculate the date range
        date_range = last_date - first_date

        if date_range < timedelta(days=365*2):
            return file_path
        else:
            pass
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False  # In case of error, don't count the file

def process_files(folder_path):
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    with Pool() as pool:
        results = pool.map(check_date_range, file_paths)
        results = [item for item in results if item is not None]

    return results

if __name__ == '__main__':
    # Specify the path to your 'stocks' folder
    folder_path = 'stocks'

    # Get the count
    names = pd.DataFrame(process_files(folder_path), columns=["Files to be deleted"])
    names.to_csv("to_be_deleted.csv")