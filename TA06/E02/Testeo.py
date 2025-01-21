import os
from datetime import datetime
import numpy as np

MONTH_NAMES = {
    '1': 'January', '2': 'February', '3': 'March', '4': 'April',
    '5': 'May', '6': 'June', '7': 'July', '8': 'August',
    '9': 'September', '10': 'October', '11': 'November', '12': 'December'
}

def validate_file(file_path, expected_header, log_file, annual_precipitation, data_count, station_precipitation, monthly_precipitation):
    is_valid = True
    total_days = 0
    invalid_days = 0
    station_total_precipitation = 0
    try:
        with open(file_path, 'r') as file:
            header1 = file.readline().strip()
            header2 = file.readline().strip()

            if header1 != expected_header:
                log_file.write(f"{file_path}: Invalid first header line\n")
                is_valid = False

            for line_num, line in enumerate(file, start=3):
                columns = line.strip().split()
                if len(columns) != 34:
                    log_file.write(f"{file_path}: Line {line_num} has {len(columns)} columns instead of 34\n")
                    is_valid = False

                year = columns[1]
                month = columns[2]

                if not (year.isdigit() and len(year) == 4):
                    log_file.write(f"{file_path}: Line {line_num} has invalid year '{year}'\n")
                    is_valid = False

                if not (month.isdigit() and 1 <= int(month) <= 12):
                    log_file.write(f"{file_path}: Line {line_num} has invalid month '{month}'\n")
                    is_valid = False

                for col_num, value in enumerate(columns[3:], start=4):
                    try:
                        num_value = float(value)
                        total_days += 1
                        data_count += 1
                        if num_value == -999:
                            invalid_days += 1
                        if not (num_value >= 0 or num_value == -999):
                            log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                            is_valid = False
                        if num_value != -999:
                            if year not in annual_precipitation:
                                annual_precipitation[year] = {'total_precipitation': 0, 'valid_days': 0}
                            annual_precipitation[year]['total_precipitation'] += num_value
                            annual_precipitation[year]['valid_days'] += 1
                            station_total_precipitation += num_value
                            if month not in monthly_precipitation:
                                monthly_precipitation[month] = 0
                            monthly_precipitation[month] += num_value
                    except ValueError:
                        log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                        is_valid = False

    except Exception as e:
        log_file.write(f"{file_path}: Error reading file - {e}\n")
        is_valid = False

    station_precipitation[file_path] = station_total_precipitation
    return is_valid, total_days, invalid_days, data_count

def validate_folder(folder_path, expected_header, log_file_path, stats_file_path):
    total_files = 0
    valid_files = 0
    total_days = 0
    invalid_days = 0
    annual_precipitation = {}
    data_count = 0
    station_precipitation = {}
    monthly_precipitation = {}

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
                is_valid, file_total_days, file_invalid_days, data_count = validate_file(file_path, expected_header, log_file, annual_precipitation, data_count, station_precipitation, monthly_precipitation)
                total_days += file_total_days
                invalid_days += file_invalid_days
                if is_valid:
                    valid_files += 1

        if total_days > 0:
            invalid_percentage = (invalid_days / total_days) * 100
            stats_file.write(f"Total: {invalid_days} out of {total_days} days are -999 ({invalid_percentage:.2f}%)\n")

        years = sorted(annual_precipitation.keys())
        for year in years:
            total_precipitation = annual_precipitation[year]['total_precipitation']
            valid_days = annual_precipitation[year]['valid_days']
            if valid_days > 0:
                average_precipitation = total_precipitation / valid_days
                stats_file.write(f"Year {year}: Average annual precipitation is {average_precipitation:.2f}\n")

        for i in range(1, len(years)):
            prev_year = years[i - 1]
            curr_year = years[i]
            prev_avg = annual_precipitation[prev_year]['total_precipitation'] / annual_precipitation[prev_year]['valid_days']
            curr_avg = annual_precipitation[curr_year]['total_precipitation'] / annual_precipitation[curr_year]['valid_days']
            variation_rate = curr_avg - prev_avg
            stats_file.write(f"Annual variation from {prev_year} to {curr_year}: {variation_rate:.2f}\n")

        if total_files > 0:
            valid_percentage = (valid_files / total_files) * 100
            stats_file.write(f"Percentage of valid files: {valid_percentage:.2f}%\n")

        stats_file.write(f"Number of processed data points: {data_count}\n")

        if station_precipitation:
            max_station = max(station_precipitation, key=station_precipitation.get)
            max_precipitation = station_precipitation[max_station]
            stats_file.write(f"Station with maximum precipitation: {max_station} with {max_precipitation:.2f} liters\n")

        if monthly_precipitation:
            max_month = max(monthly_precipitation, key=monthly_precipitation.get)
            max_month_precipitation = monthly_precipitation[max_month]
            max_month_name = MONTH_NAMES[max_month]
            stats_file.write(f"Month with maximum precipitation: {max_month_name} with {max_month_precipitation:.2f} liters\n")

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