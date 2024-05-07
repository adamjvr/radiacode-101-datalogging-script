# radiacode-101-datalogging-script
A phython script that uses the open source radiacode library to connect to a Radiacode 101 and log data over time into a CSV file

## Gamma Spectrum Logger Script

The **Gamma Spectrum Logger** script retrieves spectrum data from a RadiaCode device and saves it to a CSV file. This script is useful for logging gamma radiation spectrum data for analysis or record-keeping purposes.

## Usage Instructions:

### 1. Installation:

- Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- Install the required libraries using pip:
  ```bash
  pip install radiacode tqdm
  ```

### 2. Running the Script:

- Open a terminal window.

- Navigate to the directory containing the script (`gamma_spectrum_logger.py`).

- Run the script with Python:
  ```bash
  python gamma_spectrum_logger.py [--bluetooth-mac BLUETOOTH_MAC_ADDRESS] [--verbose]
  ```

  - Replace `BLUETOOTH_MAC_ADDRESS` with the Bluetooth MAC address of the RadiaCode device (optional).

  - Use the `--verbose` flag to enable verbose mode (optional).

### 3. Script Execution:

- Upon running the script, it will establish a connection with the RadiaCode device.

- If a Bluetooth MAC address is provided, it will use Bluetooth connection; otherwise, it will use USB connection.

- The script will prompt you to enter the duration in minutes to wait for the spectrum sample to settle.

- A progress bar will display the waiting progress.

- After the waiting period, the script will sample the spectrum data from the device.

- The spectrum data will be saved to a CSV file named `gamma_spectrum_sample_TIMESTAMP.csv`, where `TIMESTAMP` represents the current date and time.

## Example:

```bash
python gamma_spectrum_logger.py --bluetooth-mac 00:11:22:33:44:55 --verbose
```

This command will run the script, connecting to the RadiaCode device with the Bluetooth MAC address `00:11:22:33:44:55` in verbose mode.
