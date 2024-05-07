# Importing necessary libraries and modules
import argparse  # Module for parsing command-line arguments
import csv  # Module for handling CSV files
import datetime  # Module for managing date and time
import time  # Module for time-related functions
from radiacode import RadiaCode  # Importing the RadiaCode class from the radiacode module
from tqdm import tqdm  # Importing tqdm for displaying progress bar


# Function to write spectrum data to a CSV file
def write_spectrum_to_csv(spectrum, filename_prefix):
    """
    Write spectrum data to a CSV file.

    Args:
        spectrum: Spectrum data object containing frequency and amplitude information.
        filename_prefix (str): Prefix of the CSV file name.
    """
    # Get the current date and time
    now = datetime.datetime.now()
    # Format the date and time as string
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # Construct the filename with the timestamp appended
    filename_with_timestamp = f"{filename_prefix}_{timestamp}.csv"

    # Open the CSV file for writing with newline='' to prevent extra line breaks
    with open(filename_with_timestamp, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)  # Create a CSV writer object
        writer.writerow(['Timestamp', 'Frequency (MeV)', 'Amplitude'])  # Write header row

        # Calculate the duration of the spectrum data in seconds
        duration_seconds = spectrum.duration.total_seconds()

        # Iterate over each count in the spectrum data
        for i, count in enumerate(spectrum.counts):
            # Calculate the frequency in MeV using the spectrum_channel_to_energy function
            freq_kEv = spectrum_channel_to_energy(i, spectrum.a0, spectrum.a1, spectrum.a2)
            freq_MeV = freq_kEv / 1000  # Convert from keV to MeV

            # Calculate the amplitude by dividing the count by the duration
            amplitude = count / duration_seconds

            # Write the timestamp, frequency (in MeV), and amplitude to a row in the CSV file
            writer.writerow([now, freq_MeV, amplitude])

    # Print a message indicating where the spectrum data was written
    print(f'Spectrum data written to {filename_with_timestamp}')


# Function to convert spectrum channel number to energy (in keV)
def spectrum_channel_to_energy(channel_number: int, a0: float, a1: float, a2: float) -> float:
    """
    Convert spectrum channel number to energy (in keV) using calibration coefficients.

    Args:
        channel_number (int): Channel number from the spectrum data.
        a0 (float): Calibration coefficient.
        a1 (float): Calibration coefficient.
        a2 (float): Calibration coefficient.

    Returns:
        float: Energy corresponding to the channel number in keV.
    """
    return a0 + a1 * channel_number + a2 * channel_number * channel_number


if __name__ == "__main__":
    # Create an argument parser object with a description of the script
    parser = argparse.ArgumentParser(description="Retrieve spectrum data from RadiaCode device and save it to a CSV file")

    # Add optional arguments for Bluetooth MAC address and verbose mode
    parser.add_argument('--bluetooth-mac', type=str, required=False, help='Bluetooth MAC address of radiascan device')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Establish connection to the RadiaCode device based on the provided Bluetooth MAC address
    if args.bluetooth_mac:
        print('Using Bluetooth connection...')
        radiacode_device = RadiaCode(bluetooth_mac=args.bluetooth_mac)
    else:
        print('Using USB connection...')
        radiacode_device = RadiaCode()

    # Get serial number of the device and print it
    serial = radiacode_device.serial_number()
    print(f'Device serial number: {serial}')

    # Get firmware version of the device and print it
    fw_version = radiacode_device.fw_version()
    print(f'Device firmware version: {fw_version}')

    # Ask the user for the duration to wait before taking the sample
    wait_time_minutes = int(input("How many minutes to wait for the spectrum sample to settle: "))

    # Convert wait time to seconds
    wait_time_seconds = wait_time_minutes * 60

    # Display progress bar while waiting
    for _ in tqdm(range(wait_time_seconds), desc="Waiting", unit="seconds"):
        time.sleep(1)  # Wait for 1 second

    print("Sampling spectrum...")

    # Get spectrum data from the device
    spectrum = radiacode_device.spectrum()

    # Write spectrum data to CSV file
    write_spectrum_to_csv(spectrum, 'gamma_spectrum_sample')
