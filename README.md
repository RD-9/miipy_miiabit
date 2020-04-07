# MiiPy - MiiA.bit

A Python API Extension to enable support for programming your MiiA.bit robot using the Python programming language.

# Files

|                File                    |Description                         |
|----------------|-------------------------------|-----------------------------|
|miipy_miiabit.py                		 |The MiiPy Python API            |'Isn't this fun?'
|miia_bit_definitions.py         		 |A Python file containing constants and definitions for the MiiA.bit Platform.
|miia_bit_miipy_firmware_v1.1.ino        |MiiPy Compatible Firmware for the MiiA.bit Robot|

## Getting Started

 1. Upload the MiiPy Compatible Firmware to your MiiA.bit Robot
 2. Download the **miipy_miiabit.py** and **miia_bit_definitions.py** files to your computer
 3. Connect your MiiA.bit Robot to your computer **via the USB cable** and ensure the Bluetooth Control Switch is set to 'Off'

## Using the API
Creating a MiiA.bit Object:

    import miipy_miiabit.py as miia
    device = '/dev/cu.usbserial-DN0123SUBQ'
    robot = miia.MiiABit(device=device)

Once the object is created, you have access to various methods that can control various components of the robot:

    robot.control_rgb_led(red=12, green=0, blue=90)
    robot.control_servo_motor(85)
    robot.control_motor(motor='a', direction='forward', speed=19)

You can also get sensor data from the robot and update object attributes:

    robot.get_data_from_sensors()
    robot.input_button_state # object attribute that stores the input button state
    robot.distance_sensor # object attribute that stores the value from the distance sensor

## Help
You are encouraged to inspect the **miipy_miiabit.py** file for helpful docstrings explaining the usage of all the methods and attributes available to you.
