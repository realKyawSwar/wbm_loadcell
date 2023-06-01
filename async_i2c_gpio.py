import asyncio
import smbus2
import datetime
import RPi.GPIO as GPIO

# I2C addresses of the devices you want to communicate with
DEVICE_ADDRESSES = [0x12, 0x34, 0x56, 0x78]

# I2C bus number
I2C_BUS = 1

# Register addresses for data retrieval
DATA_REGISTERS = [0x00, 0x01, 0x02, 0x03]

# File prefix for storing the logged data
LOG_FILE_PREFIX = "data_log_device_"

# GPIO pins for device activation
DEVICE_PINS = [2, 3, 4, 5]

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DEVICE_PINS, GPIO.IN)


async def read_sensor_data(device_address, data_register, log_file):
    bus = smbus2.SMBus(I2C_BUS)
    while True:
        # Read data from the I2C device only when the corresponding GPIO pin is high
        if GPIO.input(DEVICE_PINS[DEVICE_ADDRESSES.index(device_address)]):
            # Read data from the I2C device
            data = bus.read_i2c_block_data(device_address, data_register, 2)

            # Convert the data to a meaningful format (assuming it's a 16-bit value)
            sensor_value = (data[0] << 8) | data[1]

            # Log the data along with the timestamp
            timestamp = datetime.datetime.now().isoformat()
            log_entry = f"{timestamp},{sensor_value}\n"

            with open(log_file, "a") as f:
                f.write(log_entry)

            # Perform real-time data analysis on the sensor value
            # Modify this section according to your analysis requirements
            analysis_result = sensor_value * 2
            print(f"Device: {hex(device_address)}, Sensor Value: {sensor_value}, Analysis Result: {analysis_result}")

        await asyncio.sleep(1)  # Wait for 1 second before reading the sensor again


async def main():
    tasks = []
    for i in range(len(DEVICE_ADDRESSES)):
        device_address = DEVICE_ADDRESSES[i]
        data_register = DATA_REGISTERS[i]
        log_file = f"{LOG_FILE_PREFIX}{hex(device_address)}.csv"
        task = asyncio.create_task(read_sensor_data(device_address, data_register, log_file))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
