import smbus2 as smb
import time

# This script reads out a BMI323 chip on a raspiberry pi zero. It continuously prints out accelerometer and gyro data

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  In my case address of the chip, but that's because I pulled SDA to GND. You might have to use 0x69 or consider the
#  documentation
address = 0x68

# Register addresses (with "normal mode" power-down bits)
reg_chip_id = 0x00
reg_device_status = 0x01
reg_sensor_status = 0x02
reg_acc_data_x = 0x03
reg_acc_data_y = 0x04
reg_acc_data_z = 0x05
reg_gyr_data_x = 0x06
reg_gyr_data_y = 0x07
reg_gyr_data_z = 0x08

# Initialize I2C (SMBus)
bus = smb.SMBus(channel)
bus.open(channel)
time.sleep(1.0)

# Check chip status and initialization
chip_id = bus.read_i2c_block_data(address, reg_chip_id, 4)
time.sleep(0.1)
device_status = bus.read_i2c_block_data(address, reg_device_status, 4) # expected to be 0b0
time.sleep(0.1)
sensor_status = bus.read_i2c_block_data(address, reg_sensor_status, 4) # expected to be 0b1 according to doc, but i think 0b0 can also be ok
time.sleep(0.1)

print("chip id", chip_id)
print("device status", device_status)
print("sensor status", sensor_status)

# configure for normal power mode
acc_config = bus.read_i2c_block_data(address, 0x20, 4)
acc_config_int = int.from_bytes(acc_config[2:], byteorder='little', signed=False)
print("acc config", acc_config, acc_config[2:], format(acc_config_int,'x'), format(acc_config_int,'b'))

bus.write_i2c_block_data(address, 0x20, [0x27,0x40])#[0x4027])
time.sleep(0.1)
acc_config = bus.read_i2c_block_data(address, 0x20, 4)
acc_config_int = int.from_bytes(acc_config[2:], byteorder='little', signed=False)
print("acc config", acc_config, acc_config[2:], format(acc_config_int,'x'), format(acc_config_int,'b'))
time.sleep(0.1)

print("---")
gyr_config = bus.read_i2c_block_data(address, 0x21, 4)
print("gyr config", gyr_config)
time.sleep(0.1)
bus.write_i2c_block_data(address, 0x21, [0x4b,0x40])
gyr_config = bus.read_i2c_block_data(address, 0x21, 4)
print("gyr config", gyr_config)
time.sleep(0.1)

print("--- Initialized correctly ---")

#bus.write_i2c_block_data(address, 0x7E, [0xDEAF]) # soft reset
#bus.close()
#print("bye bye")
#exit()

for i in range(1000):
    acc_data = bus.read_i2c_block_data(address, reg_acc_data_x, 8)
    acc_data_x = int.from_bytes(acc_data[2:4], byteorder='little', signed=True)
    acc_data_y = int.from_bytes(acc_data[4:6], byteorder='little', signed=True)
    acc_data_z = int.from_bytes(acc_data[6:8], byteorder='little', signed=True)
    #time.sleep(0.1)
    gyr_data = bus.read_i2c_block_data(address, reg_gyr_data_x, 8)
    gyr_data_x = int.from_bytes(gyr_data[2:4], byteorder='little', signed=True)
    gyr_data_y = int.from_bytes(gyr_data[4:6], byteorder='little', signed=True)
    gyr_data_z = int.from_bytes(gyr_data[6:8], byteorder='little', signed=True)
    #time.sleep(0.1)
    #acc_data_y = bus.read_i2c_block_data(address, reg_acc_data_y, 4)
    #acc_data_z = bus.read_i2c_block_data(address, reg_acc_data_z, 4)
    time0 = bus.read_i2c_block_data(address, 0xA, 4)
    time1 = bus.read_i2c_block_data(address, 0xB, 4)
    time_bmi323 = int.from_bytes(time0+time1, byteorder='little', signed=False)
    time.sleep(.1)
    print(acc_data_x, "\t", acc_data_y, "\t", acc_data_z, "\t", gyr_data_x, "\t", gyr_data_y, "\t", gyr_data_z, "\t", time_bmi323)#, acc_data_y, acc_data_z)


bus.write_i2c_block_data(address, 0x7E, [0xDEAF]) # soft reset
bus.close()
print("bye bye")

# # Create a sawtooth wave 16 times
# for i in range(0x10000):
#
#     # Create our 12-bit number representing relative voltage
#     voltage = i & 0xfff
#
#     # Shift everything left by 4 bits and separate bytes
#     msg = (voltage & 0xff0) >> 4
#     msg = [msg, (msg & 0xf) << 4]
#
#     # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
#     bus.write_i2c_block_data(address, reg_write_dac, msg)
