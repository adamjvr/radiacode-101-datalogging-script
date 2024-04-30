import csv  # Importing the CSV module for handling CSV files
import time  # Importing the time module for timestamping
import radiacode  # Importing the radiacode library for interfacing with the Radiacode 101 device

# Function to sample radiation data and record it in a CSV file
def sample_radiation_data(num_samples, sample_interval, csv_filename):
    # Open the CSV file in write mode with newline='' to ensure proper line endings
    with open(csv_filename, 'w', newline='') as csvfile:
        # Define the field names for the CSV file
        fieldnames = ['timestamp', 'radiation_level']
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row to the CSV file
        writer.writeheader()

        # Initialize the Radiacode 101 device
        radiacode_device = radiacode.Radiacode101()

        # Loop to sample radiation data for the specified number of samples
        for _ in range(num_samples):
            # Sample the radiation level from the Radiacode 101 device
            radiation_level = radiacode_device.sample()
            # Get the current timestamp
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            # Write the timestamp and radiation level to the CSV file
            writer.writerow({'timestamp': timestamp, 'radiation_level': radiation_level})
            # Wait for the specified interval between samples
            time.sleep(sample_interval)

# Main function
if __name__ == "__main__":
    # Prompt the user to input the number of samples to take
    num_samples = int(input("Enter the number of samples to take: "))
    # Prompt the user to input the time interval between samples (in seconds)
    sample_interval = int(input("Enter the time interval between samples (in seconds): "))
    # Prompt the user to input the name of the CSV file to save data to
    csv_filename = input("Enter the name of the CSV file to save data to: ")

    # Call the function to sample radiation data and record it in the CSV file
    sample_radiation_data(num_samples, sample_interval, csv_filename)
