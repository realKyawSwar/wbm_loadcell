import smbus2
import time
import csv
from scipy import stats

# Define the I2C bus number (e.g., 1 for Raspberry Pi 3 and 4, 0 for older models)
i2c_bus = 1

# Define the I2C address of your ADC device
adc_address = 0x48

# Define the channels you want to read from (0-3 for a 4-channel ADC)
channels = [0, 1, 2, 3]

# Define the CSV file path for storing the data
csv_file_path = 'adc_data.csv'

# Define the sampling interval in seconds
sampling_interval = 0.01  # Sample every 10 milliseconds

# Define the duration for storing data in seconds
data_duration = 30

# Open the I2C bus
bus = smbus2.SMBus(i2c_bus)

# Create a CSV file and write the header
with open(csv_file_path, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Timestamp'] + ['Channel {}'.format(ch) for ch in channels] + ['Mean', 'Median', 'Standard Deviation'])

    # Store the start time
    start_time = time.time()

    # Read and log the ADC data for the specified duration
    while time.time() - start_time <= data_duration:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Read ADC data from each channel
        adc_data = []
        for ch in channels:
            # Read the 16-bit ADC value
            raw_value = bus.read_word_data(adc_address, ch)

            # Swap bytes to get the correct value
            value = ((raw_value & 0xFF) << 8) | (raw_value >> 8)

            # Store the converted ADC value
            adc_data.append(value)

        # Perform real-time analysis on the ADC data
        mean = stats.mean(adc_data)
        median = stats.median(adc_data)
        std_dev = stats.stdev(adc_data)

        # Write the timestamp, ADC data, and analysis results to the CSV file
        writer.writerow([timestamp] + adc_data + [mean, median, std_dev])
        csv_file.flush()

        # Wait for the next sampling interval
        time.sleep(sampling_interval)
