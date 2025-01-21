import os
from datetime import datetime
import numpy as np

def validate_file(file_path, expected_header, log_file, annual_precipitation):
    """
    Validates a file with space-separated values and logs statistics.

    Parameters:
    file_path (str): The path to the file to be validated.
    expected_header (str): The expected first line of the header.
    log_file (file object): The file object to log errors.
    annual_precipitation (dict): Dictionary to accumulate annual precipitation.

    Returns:
    tuple: (bool, int, int) True if the file is valid, False otherwise, total days, and invalid days.
    """
    is_valid = True
    total_days = 0
    invalid_days = 0
    try:
        with open(file_path, 'r') as file:
            # Read the first two lines (headers)
            header1 = file.readline().strip()
            header2 = file.readline().strip()

            # Validate the first header line
            if header1 != expected_header:
                log_file.write(f"{file_path}: Invalid first header line\n")
                is_valid = False

            # Validate the data lines
            for line_num, line in enumerate(file, start=3):
                columns = line.strip().split()
                # Validate the number of columns
                if len(columns) != 34:
                    log_file.write(f"{file_path}: Line {line_num} has {len(columns)} columns instead of 34\n")
                    is_valid = False

                year = columns[1]
                month = columns[2]

                # Validate year (4 digits)
                if not (year.isdigit() and len(year) == 4):
                    log_file.write(f"{file_path}: Line {line_num} has invalid year '{year}'\n")
                    is_valid = False

                # Validate month (1-12)
                if not (month.isdigit() and 1 <= int(month) <= 12):
                    log_file.write(f"{file_path}: Line {line_num} has invalid month '{month}'\n")
                    is_valid = False

                # Validate the remaining 31 columns
                for col_num, value in enumerate(columns[3:], start=4):
                    try:
                        num_value = float(value)
                        total_days += 1
                        if num_value == -999:
                            invalid_days += 1
                        if not (num_value >= 0 or num_value == -999):
                            log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                            is_valid = False
                        if num_value != -999:
                            if year not in annual_precipitation:
                                annual_precipitation[year] = []
                            annual_precipitation[year].append(num_value)
                    except ValueError:
                        log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                        is_valid = False

    except Exception as e:
        log_file.write(f"{file_path}: Error reading file - {e}\n")
        is_valid = False

    return is_valid, total_days, invalid_days

def validate_folder(folder_path, expected_header, log_file_path, stats_file_path):
    """
    Validates all files in a folder with space-separated values and calculates the percentage of valid files.

    Parameters:
    folder_path (str): The path to the folder containing the files to be validated.
    expected_header (str): The expected first line of the header for all files.
    log_file_path (str): The path to the log file.
    stats_file_path (str): The path to the statistics log file.

    Returns:
    float: The percentage of valid files.
    """
    total_files = 0
    valid_files = 0
    total_days = 0
    invalid_days = 0
    annual_precipitation = {}

    with open(log_file_path, 'a') as log_file, open(stats_file_path, 'a') as stats_file:
        log_file.write(f"\nLog Date: {datetime.now()}\n")
        stats_file.write(f"\nStatistics Date: {datetime.now()}\n")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith('.dat'):
                    log_file.write(f"{os.path.join(root, file)}: Invalid file format\n")
                    continue

                file_path = os.path.join(root, file)
                total_files += 1
                is_valid, file_total_days, file_invalid_days = validate_file(file_path, expected_header, log_file, annual_precipitation)
                total_days += file_total_days
                invalid_days += file_invalid_days
                if is_valid:
                    valid_files += 1

        if total_days > 0:
            invalid_percentage = (invalid_days / total_days) * 100
            stats_file.write(f"Total: {invalid_days} out of {total_days} days are -999 ({invalid_percentage:.2f}%)\n")

        # Calculate and log the average annual precipitation
        for year, precipitations in annual_precipitation.items():
            average_precipitation = np.mean(precipitations)
            stats_file.write(f"Year {year}: Average annual precipitation is {average_precipitation:.2f}\n")

        # Calculate and log the percentage of valid files
        if total_files > 0:
            valid_percentage = (valid_files / total_files) * 100
            stats_file.write(f"Percentage of valid files: {valid_percentage:.2f}%\n")

    if total_files == 0:
        return 0.0

    return (valid_files / total_files) * 100

# Example usage
folder_path = '../../prova'
expected_header = 'precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1'
log_file_path = 'RegistroErroresValidacion.log'
stats_file_path = 'EstadisticasValidacion.log'
valid_percentage = validate_folder(folder_path, expected_header, log_file_path, stats_file_path)
print(f"Percentage of valid files: {valid_percentage:.2f}%")
print(f"Log file: {log_file_path}")
print(f"Statistics file: {stats_file_path}")