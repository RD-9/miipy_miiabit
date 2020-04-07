__name__ = "miia_bit_definitions"
__author__ = "tyronevb"
__data__ = "april 2020"


# serial connection defaults
BAUD_RATE = 57600
TIMEOUT = 0.1

# dictionary with op codes
miia_bit_opcodes = {
    "buzzer": 201,
    "motor_a": 202,
    "motor_b": 203,
    "rgb_led_r": 204,
    "rgb_led_g": 205,
    "rgb_led_b": 206,
    "servo": 208,
}

# available motors on miia.bit
miia_bit_motors = ['a', 'b']

# valid ranges for settings
miia_bit_motor_speed_range = range(0, 101)

miia_bit_motor_directions = {'reverse': 1,
                             'forward': 0}

miia_bit_buzzer_states = {'on': 1,
                          'off': 0}

miia_bit_servo_range = range(0, 101)

miia_bit_calibration_range = range(-50, 51)

miia_bit_rgb_led_range = range(0, 101)

# end
