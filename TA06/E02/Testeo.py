import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv

MONTH_NAMES = {
    '1': 'January', '2': 'February', '3': 'March', '4': 'April',
    '5': 'May', '6': 'June', '7': 'July', '8': 'August',
    '9': 'September', '10': 'October', '11': 'November', '12': 'December'
}

def validate_file(file_path, expected_header, log_file, annual_precipitation, data_count, station_precipitation, monthly_precipitation, monthly_totals):
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
                                annual_precipitation[year] = {}
                            if file_path not in annual_precipitation[year]:
                                annual_precipitation[year][file_path] = 0
                            annual_precipitation[year][file_path] += num_value
                            station_total_precipitation += num_value
                            if file_path not in monthly_precipitation:
                                monthly_precipitation[file_path] = {}
                            if month not in monthly_precipitation[file_path]:
                                monthly_precipitation[file_path][month] = 0
                            monthly_precipitation[file_path][month] += num_value
                            if month not in monthly_totals:
                                monthly_totals[month] = {'total': 0, 'count': 0}
                            monthly_totals[month]['total'] += num_value
                            monthly_totals[month]['count'] += 1
                    except ValueError:
                        log_file.write(f"{file_path}: Line {line_num} column {col_num} has invalid value '{value}'\n")
                        is_valid = False

    except Exception as e:
        log_file.write(f"{file_path}: Error reading file - {e}\n")
        is_valid = False

    station_precipitation[file_path] = station_total_precipitation
    return is_valid, total_days, invalid_days, data_count

def plot_statistics(year_avg_precipitation, monthly_totals, output_path):
    years = list(year_avg_precipitation.keys())
    avg_precipitation = list(year_avg_precipitation.values())

    plt.figure(figsize=(10, 5))

    # Plot average annual precipitation
    plt.subplot(1, 2, 1)
    plt.bar(years, avg_precipitation, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Average Annual Precipitation (liters)')
    plt.title('Average Annual Precipitation')

    # Plot average monthly precipitation
    months = [MONTH_NAMES[str(i)] for i in range(1, 13)]
    avg_monthly_precipitation = [monthly_totals[str(i)]['total'] / monthly_totals[str(i)]['count'] for i in range(1, 13)]

    plt.subplot(1, 2, 2)
    plt.bar(months, avg_monthly_precipitation, color='green')
    plt.xlabel('Month')
    plt.ylabel('Average Monthly Precipitation (liters)')
    plt.title('Average Monthly Precipitation')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

def validate_folder(folder_path, expected_header, log_file_path, stats_file_path):
    total_files = 0
    valid_files = 0
    total_days = 0
    invalid_days = 0
    annual_precipitation = {}
    data_count = 0
    station_precipitation = {}
    monthly_precipitation = {}
    monthly_totals = {}

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
                is_valid, file_total_days, file_invalid_days, data_count = validate_file(file_path, expected_header, log_file, annual_precipitation, data_count, station_precipitation, monthly_precipitation, monthly_totals)
                total_days += file_total_days
                invalid_days += file_invalid_days
                if is_valid:
                    valid_files += 1

        if total_days > 0:
            invalid_percentage = (invalid_days / total_days) * 100
            valid_percentage_days = 100 - invalid_percentage
            stats_file.write(f"Percentage of valid days: {valid_percentage_days:.2f}%\n")
            stats_file.write(f"Percentage of invalid days: {invalid_percentage:.2f}%\n")

        if total_files > 0:
            valid_percentage_files = (valid_files / total_files) * 100
            stats_file.write(f"Percentage of valid files: {valid_percentage_files:.2f}%\n")

        stats_file.write(f"Number of processed data points: {data_count}\n")

        years = sorted(annual_precipitation.keys())
        year_avg_precipitation = {}
        for year in years:
            total_precipitation = sum(annual_precipitation[year].values())
            num_stations = len(annual_precipitation[year])
            average_precipitation = (total_precipitation / num_stations) / 12
            year_avg_precipitation[year] = average_precipitation

        sorted_years = sorted(year_avg_precipitation.items(), key=lambda x: x[1], reverse=True)
        top_three_years = sorted_years[:3]
        bottom_three_years = sorted_years[-3:]

        stats_file.write("Top 3 years with most precipitation:\n")
        for year, avg_precip in top_three_years:
            stats_file.write(f"  Year {year}: {avg_precip:.2f} liters\n")

        stats_file.write("Top 3 driest years:\n")
        for year, avg_precip in bottom_three_years:
            stats_file.write(f"  Year {year}: {avg_precip:.2f} liters\n")

        stats_file.write("Average monthly precipitation across all stations:\n")
        for month, totals in sorted(monthly_totals.items()):
            month_name = MONTH_NAMES[month]
            avg_precip = totals['total'] / totals['count']
            stats_file.write(f"  {month_name}: {avg_precip:.2f} liters per day\n")

        for year in years:
            total_precipitation = sum(annual_precipitation[year].values())
            num_stations = len(annual_precipitation[year])
            average_precipitation = (total_precipitation / num_stations) / 12
            stats_file.write(f"Year {year}: Total precipitation is {total_precipitation:.2f} liters, Average annual precipitation is {average_precipitation:.3f} liters\n")

        for i in range(1, len(years)):
            prev_year = years[i - 1]
            curr_year = years[i]
            prev_total = sum(annual_precipitation[prev_year].values())
            curr_total = sum(annual_precipitation[curr_year].values())
            variation = (curr_total - prev_total) / 12
            stats_file.write(f"Annual variation from {prev_year} to {curr_year}: {variation:.2f} liters\n")

    plot_statistics(year_avg_precipitation, monthly_totals, '../E03/statistics_plot.png')

    # Print summary statistics to the terminal
    print(f"Percentage of valid files: {valid_percentage_files:.2f}%")
    print(f"Percentage of valid days: {valid_percentage_days:.2f}%")
    print(f"Number of processed data points: {data_count}")
    print("Top 3 years with most precipitation:")
    for year, avg_precip in top_three_years:
        print(f"  Year {year}: {avg_precip:.2f} liters")
    print("Top 3 driest years:")
    for year, avg_precip in bottom_three_years:
        print(f"  Year {year}: {avg_precip:.2f} liters")

    # Export summary statistics to CSV
    csv_output_path = '../E03/summary_statistics.csv'
    with open(csv_output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Type', 'Data'])
        csvwriter.writerow(['Percentage of valid files', f"{valid_percentage_files:.2f}%"])
        csvwriter.writerow(['Percentage of valid days', f"{valid_percentage_days:.2f}%"])
        csvwriter.writerow(['Number of processed data points', data_count])
        csvwriter.writerow(['Top 3 years with most precipitation'])
        for year, avg_precip in top_three_years:
            csvwriter.writerow(['Year', year])
            csvwriter.writerow(['Average Precipitation', f"{avg_precip:.2f} liters"])
        csvwriter.writerow(['Top 3 driest years'])
        for year, avg_precip in bottom_three_years:
            csvwriter.writerow(['Year', year])
            csvwriter.writerow(['Average Precipitation', f"{avg_precip:.2f} liters"])

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
print(f"Summary statistics CSV file: ../E03/summary_statistics.csv")