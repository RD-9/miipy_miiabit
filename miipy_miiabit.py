__name__ = "miipy_miiabit"
__author__ = "tyronevb"
__data__ = "april 2020"

# library imports
import serial
import struct
import miia_bit_definitions as mbd


class MiiABit(object):
    def __init__(self, device, baud_rate=mbd.BAUD_RATE, timeout=mbd.TIMEOUT,
                 motor_a_calibration=0, motor_b_calibration=0):
        """
        Create a new MiiA.bit Object for programming via USB serial cable
        :param device: serial device name of the robot when connected via USB
        :param baud_rate: rate of communication, defaults to MiiA.bit default
        :param timeout: timeout for communication, defaults to MiiA.bit default
        :param motor_a_calibration: calibration factor for motor a
        :param motor_b_calibration: calibration factor for motor b
        """

        # serial connection configuration
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout

        # establish connection to port and open the port
        self.serial_connection = serial.Serial(port=self.device,
                                               baudrate=self.baud_rate,
                                               timeout=self.timeout)

        # dictionary of calibration values for easier housekeeping
        # set the calibration values if given at object creation
        self.motor_cal_values = {'a': motor_a_calibration,
                                 'b': motor_b_calibration}

        # attributes to store data received from the robot
        # initialized to None as to not assume state
        self.distance_sensor = None
        self.input_button_state = None

        # ensure things are settled and the serial port is active
        self._connection_ready()

    def _close(self):
        """
        Close the serial connection/port to the device
        :return:
        """

        self.serial_connection.close()

    def _open(self):
        """
        Open the serial connection/port to the device
        :return:
        """

        self.serial_connection.open()

    def get_data_from_sensors(self):
        """
        Get the values from the Ultrasonic Sensor and Input Button
        and assign them to object attributes
        :return:
        """

        self._receive_data()

    def set_motor_calibration(self, motor, calibration_factor=0):
        """
        Calibrate motor on the MiiA Robots.
        :param motor: Options: 'a' or 'b'
        :param calibration_factor: Value in the range -50 to 50
        :return:
        """

        assert motor in mbd.miia_bit_motors, \
            "Select either motor a or b"
        assert calibration_factor in mbd.miia_bit_calibration_range, \
            "Calibration factor must be in the range -50 to 50"

        self.motor_cal_values[motor] = calibration_factor

    def control_rgb_led(self, red=0, green=0, blue=0):
        """
        Control the RGB LED on the MiiA robots. Takes individual intensity
        values for each colour channel and mixes them to produce a new colour.
        Intensity values must be in the range of 0 to 100.
        To turn the LED off, set an intensity of 0 on each channel.
        :param red: intensity for red channel
        :param green: intensity for green channel
        :param blue: intensity for blue channel
        :return:
        """

        assert red in mbd.miia_bit_rgb_led_range, \
            "Channel intensity must be between 0 and 100"
        assert green in mbd.miia_bit_rgb_led_range, \
            "Channel intensity must be between 0 and 100"
        assert blue in mbd.miia_bit_rgb_led_range, \
            "Channel intensity must be between 0 and 100"

        # create data structure
        data_array = [mbd.miia_bit_opcodes['rgb_led_r'], red,
                      mbd.miia_bit_opcodes['rgb_led_g'], green,
                      mbd.miia_bit_opcodes['rgb_led_b'], blue]

        # pack data
        packed_data_array = self._pack_data_array(*data_array)

        # send data
        self._send_data(packed_data_array)

    def control_buzzer(self, buzzer_state=None):
        """
        Control the buzzer on the MiiA robot. Takes in a buzzer state which
        is either on or off.
        :param buzzer_state: 'on' - buzzer on, 'off' - buzzer off
        :return:
        """

        assert buzzer_state in mbd.miia_bit_buzzer_states.keys(), \
            "Buzzer state must be 'on' or 'off'"

        # create data structure
        data_array = [mbd.miia_bit_opcodes['buzzer'],
                      mbd.miia_bit_buzzer_states[buzzer_state]]

        # pack data
        packed_data_array = self._pack_data_array(*data_array)

        # send data
        self._send_data(packed_data_array)

    def control_motor(self, motor, direction, speed):
        """
        Control a motor on the MiiA robots. Takes a motor, direction indicator,
        and speed value.
        :param motor: a motor on the MiiA Robot: either 'a' or 'b'
        :param direction: 'forward' or 'reverse'
        :param speed: Value between 0 and 100
        :return:
        """

        # replace this with a constant def that can be maintained
        assert direction in mbd.miia_bit_motor_directions, \
            "Direction must be either 'forward' or 'reverse"
        assert speed in mbd.miia_bit_motor_speed_range, \
            "Speed must be in the range 0 - 100"
        assert motor in mbd.miia_bit_motors, \
            "Select either motor a or b"

        selected_motor = 'motor_{}'.format(motor)

        # add motor calibration factor
        speed += self.motor_cal_values[motor]

        # create data structure
        data_array = [mbd.miia_bit_opcodes[selected_motor],
                      mbd.miia_bit_motor_directions[direction],
                      speed]

        # pack data
        packed_data_array = self._pack_data_array(*data_array)

        # send data
        self._send_data(packed_data_array)

    def control_servo_motor(self, position):
        """
        Control the Positional Servo Motor on the MiiA robots. Takes in a
        position that maps to a value between 0 - 180 in degrees.
        :param position: In the range 0 - 100. Maps to the range 0 - 180.
        :return:
        """

        assert position in mbd.miia_bit_servo_range, \
            "Position must be in the range 0 - 100"
        
        # create data structure
        data_array = [mbd.miia_bit_opcodes['servo'], position]

        # pack data
        packed_data_array = self._pack_data_array(*data_array)

        # send data
        self._send_data(packed_data_array)

    def _receive_data(self):
        """
        Receive data from robot via serial connection
        :return: received data array
        """
        rcvd = struct.unpack("!6B", self.serial_connection.read(size=6))
        # data is returned as [99, input_button, 99, 122, distance, 122]

        # set received input button value
        self.input_button_state = rcvd[1]

        # set received distance sensor value
        self.distance_sensor = rcvd[4]

    def _send_data(self, data_array):
        """
        Sends data to robot via serial connection.
        :param data_array: array of data to send
        :return:
        """

        for item in data_array:
            self.serial_connection.write(item)

    @staticmethod
    def _pack_data_array(*data):
        """
        Create the data array to send to the robot. Packs in binary format
        :param data: data to be sent to the robot
        :return: packed_data_array - array containing binary packed data
        """

        packed_data_array = []

        for item in data:
            packed_data_array.append(struct.pack("!1B", item))

        return packed_data_array

    def _connection_ready(self):
        """
        Send some dummy data to ensure things are settled and the serial
        port is active
        :return:
        """

        data = self._pack_data_array(0)

        self._send_data(data)

# end
