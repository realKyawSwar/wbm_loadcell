import asyncio
import smbus2
import datetime

# I2C address of the device you want to communicate with
DEVICE_ADDRESS = 0x12

# I2C bus number
I2C_BUS = 1

# Register addresses for data retrieval
DATA_REGISTER = 0x00

# File to store the logged data
LOG_FILE = "data_log.csv"


async def read_sensor_data():
    bus = smbus2.SMBus(I2C_BUS)
    while True:
        # Read data from the I2C device
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, DATA_REGISTER, 2)
        
        # Convert the data to a meaningful format (assuming it's a 16-bit value)
        sensor_value = (data[0] << 8) | data[1]
        
        # Log the data along with the timestamp
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"{timestamp},{sensor_value}\n"
        
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        
        await asyncio.sleep(1)  # Wait for 1 second before reading the sensor again


async def main():
    # Start the data logging task
    logging_task = asyncio.create_task(read_sensor_data())
    
    # Add other tasks if needed
    
    # Wait for all tasks to complete
    await asyncio.gather(logging_task)


if __name__ == "__main__":
    asyncio.run(main())
