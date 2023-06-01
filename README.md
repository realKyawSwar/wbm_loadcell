# wbm_loadcell
perform real time data collection, data analysis and IO integration with PLC

for multi_async_i2c_comm.py

In this modified code, we have introduced lists to store the I2C addresses (DEVICE_ADDRESSES), data registers (DATA_REGISTERS), and log file names (LOG_FILE_PREFIX). The lists are assumed to be in the same order, where the ith element of each list corresponds to the ith I2C device.

The read_sensor_data function is still an asynchronous task, but now it takes additional parameters for the specific device's address, data register, and log file name. Inside this function, you can perform real-time data analysis on the sensor value before logging it. Modify the data analysis section according to your specific requirements.

In the main function, we create a separate task for each device by iterating over the lists of addresses, data registers, and log file names. Each task corresponds to one device and runs the read_sensor_data function with the respective device's parameters. All tasks are added to the tasks list.

Finally, we use asyncio.gather(*tasks) to wait for all tasks to complete.

Make sure to adjust the DEVICE_ADDRESSES, DATA_REGISTERS, and LOG_FILE_PREFIX lists to match your specific setup. Each device will have its own log file based on its address.


For asyncio_i2c_gpio.py

added the RPi.GPIO library to handle the GPIO pins. The DEVICE_PINS list holds the GPIO pin numbers corresponding to each device. We set up the GPIO mode and configure the pins as inputs using GPIO.setmode(GPIO.BCM) and GPIO.setup(DEVICE_PINS, GPIO.IN).

Inside the read_sensor_data function, we check the corresponding GPIO pin status using GPIO.input(DEVICE_PINS[DEVICE_ADDRESSES.index(device_address)]). The DEVICE_ADDRESSES.index(device_address) finds the index of the current device address in the DEVICE_ADDRESSES list, which is then used to get the corresponding GPIO pin from the DEVICE_PINS list. If the GPIO pin is high, we proceed with reading data from the I2C device, logging it, and performing real-time analysis.

Now, only when the GPIO pin for a specific device is set to high, the corresponding device will start logging data and perform analysis. Make sure to adjust the DEVICE_ADDRESSES, DATA_REGISTERS, LOG_FILE_PREFIX, and DEVICE_PINS lists according to your specific setup.
