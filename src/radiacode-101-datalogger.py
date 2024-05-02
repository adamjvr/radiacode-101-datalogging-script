import argparse
import csv  # Importing the CSV module for handling CSV files
import time  # Importing the time module for timestamping
from datetime import datetime # Importing the datetime module for getting current time
from tqdm import tqdm  # Import tqdm for the progress bar
from radiacode import RadiaCode, DoseRateDB, RareData, RealTimeData, RawData, Event # Importing the RadiaCode class from the radiacode library

# Function to sample radiation data and record it in a CSV file
def sample_radiation_data(num_samples, sample_interval, csv_filename, radiacode, verbose=False):
    """
    Samples radiation data from the Radiacode device and records it in a CSV file.

    Args:
        num_samples (int): The number of samples to collect.
        sample_interval (float): The time interval between each sample in seconds.
        csv_filename (str): The name of the CSV file to write the data to.
        radiacode (RadiaCode): The Radiacode device object.
        verbose (bool, optional): Whether to print each data sample as it's read in. Defaults to False.

    Returns:
        None
    """
    # Define field names for CSV columns
    fieldnames = ['timestamp', 'RealTimeData', 'DoseRateDB', 'RareData', 'RawData', 'Event']

    # Open the CSV file in write mode with newline='' to ensure proper line endings
    with open(csv_filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row to the CSV file
        writer.writeheader()

        # Initialize tqdm for progress bar
        progress_bar = tqdm(total=num_samples, desc='Sampling Radiation Data', unit=' sample')

        # Loop to sample radiation data for the specified number of samples
        for sample_count in range(num_samples):
            # Sample the radiation data from the Radiacode device
            databuf = radiacode.data_buf()
            # Get the current timestamp with microseconds precision
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # Create a dictionary to store the data for the current sample
            sample_data = {'timestamp': timestamp}

            # Extract RealTimeData and add it to the sample_data dictionary
            real_time_data = next((d for d in databuf if isinstance(d, RealTimeData)), None)
            sample_data['RealTimeData'] = str(real_time_data) if real_time_data else ''  # Convert data to string if not None

            # Extract data of other types and add them to the sample_data dictionary
            for data_type in fieldnames[2:]:
                data = next((d for d in databuf if isinstance(d, globals()[data_type])), None)
                sample_data[data_type] = str(data) if data else ''  # Convert data to string if not None

            # Write the sample data to the CSV file
            writer.writerow(sample_data)

            # Print each data sample if verbose mode is enabled
            if verbose:
                print(f"Sample {sample_count + 1}: {sample_data}")

            # Update progress bar
            progress_bar.update(1)

            # Wait for the specified interval between samples
            time.sleep(sample_interval)

        # Close tqdm progress bar after completion
        progress_bar.close()

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--bluetooth-mac', type=str, required=False, help='bluetooth MAC address of radiascan device')
    parser.add_argument('--verbose', action='store_true', help='enable verbose mode')
    args = parser.parse_args()

    verbose_mode = args.verbose

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
    sample_radiation_data(num_samples, sample_interval, csv_filename, radiacode_device, verbose=verbose_mode)
