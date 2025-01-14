import os

def validate_file(file_path, expected_header, log_file):
    """
    Validates a file with space-separated values.

    Parameters:
    file_path (str): The path to the file to be validated.
    expected_header (str): The expected first line of the header.
    log_file (file object): The file object to log errors.

    Returns:
    bool: True if the file is valid, False otherwise.
    """
    is_valid = True
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
                        float(value)
                    except ValueError:
                        log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                        is_valid = False

    except Exception as e:
        log_file.write(f"{file_path}: Error reading file - {e}\n")
        is_valid = False

    return is_valid

def validate_folder(folder_path, expected_header, log_file_path):
    """
    Validates all files in a folder with space-separated values and calculates the percentage of valid files.

    Parameters:
    folder_path (str): The path to the folder containing the files to be validated.
    expected_header (str): The expected first line of the header for all files.
    log_file_path (str): The path to the log file.

    Returns:
    float: The percentage of valid files.
    """
    total_files = 0
    valid_files = 0

    with open(log_file_path, 'w') as log_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_files += 1
                if validate_file(file_path, expected_header, log_file):
                    valid_files += 1

    if total_files == 0:
        return 0.0

    return (valid_files / total_files) * 100

# Example usage
folder_path = '../../precip.MIROC5.RCP60.2006-2100.SDSM_REJ'
expected_header = 'precip\tMIROC5\tRCP60\tREGRESION\tdecimas\t1'
log_file_path = 'RegistroErroresValidacion.log'
valid_percentage = validate_folder(folder_path, expected_header, log_file_path)
print(f"Percentage of valid files: {valid_percentage:.2f}%")
print(f"Log file: {log_file_path}")