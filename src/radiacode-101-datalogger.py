import argparse
import csv  # Importing the CSV module for handling CSV files
import time  # Importing the time module for timestamping
from radiacode import RadiaCode, DoseRateDB, RareData, RealTimeData, RawData, Event # Importing the RadiaCode class from the radiacode library


import csv
import time
from datetime import datetime

# Function to sample radiation data and record it in a CSV file
def sample_radiation_data(num_samples, sample_interval, csv_filename, radiacode):
    # Open the CSV file in write mode with newline='' to ensure proper line endings
    with open(csv_filename, 'w', newline='') as csvfile:
        # Define the field names for the CSV file
        fieldnames = ['timestamp', 'radiation_type', 'data']
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row to the CSV file
        writer.writeheader()

        # Loop to sample radiation data for the specified number of samples
        for _ in range(num_samples):
            # Sample the radiation data from the Radiacode device
            databuf = radiacode.data_buf()
            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # Write each type of radiation data to the CSV file
            for data in databuf:
                if isinstance(data, DoseRateDB):
                    radiation_type = 'DoseRateDB'
                elif isinstance(data, RareData):
                    radiation_type = 'RareData'
                elif isinstance(data, RealTimeData):
                    radiation_type = 'RealTimeData'
                elif isinstance(data, RawData):
                    radiation_type = 'RawData'
                elif isinstance(data, Event):
                    radiation_type = 'Event'
                else:
                    radiation_type = 'Unknown'
                writer.writerow({'timestamp': timestamp, 'radiation_type': radiation_type, 'data': str(data)})
            # Wait for the specified interval between samples
            time.sleep(sample_interval)


# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bluetooth-mac', type=str, required=False, help='bluetooth MAC address of radiascan device')
    args = parser.parse_args()

    if args.bluetooth_mac:
        print('will use Bluetooth connection')
        radiacode_device = RadiaCode(bluetooth_mac=args.bluetooth_mac)
    else:
        print('will use USB connection')
        radiacode_device = RadiaCode()

    serial = radiacode_device.serial_number()
    print(f'### Serial number: {serial}')
    print('--------')

    fw_version = radiacode_device.fw_version()
    print(f'### Firmware: {fw_version}')
    print('--------')

    spectrum = radiacode_device.spectrum()
    print(f'### Spectrum: {spectrum}')
    print('--------')

    print('### DataBuf:')


    # Prompt the user to input the number of samples to take
    num_samples = int(input("Enter the number of samples to take: "))
    # Prompt the user to input the time interval between samples (in seconds)
    sample_interval = int(input("Enter the time interval between samples (in seconds): "))
    # Prompt the user to input the name of the CSV file to save data to
    csv_filename = input("Enter the name of the CSV file to save data to: ")

    # Call the function to sample radiation data and record it in the CSV file
    sample_radiation_data(num_samples, sample_interval, csv_filename,radiacode_device)
