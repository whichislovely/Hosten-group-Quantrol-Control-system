'''
This is an example of a config file that is used in the Hosten lab, cold atoms team.

In case you do not have digital, analog, dds, or sampler channels simply set their channels_number values to 0

Skipping images is a functionality very specific to our experimental setup. It triggers the image acquisition
camera as we observed that first several images might probabilistically be faulty. Feel free to set it to False

For the list_of_devices you can have a look at your device_db.py file to see what options do you have
'''

digital_channels_number = 16
analog_channels_number = 16
dds_channels_number = 12
sampler_channels_number = 8
package_manager = "conda" #it can be either conda or clang64
artiq_environment_name = "artiq_5" # it can be either artiq or artiq_5 for Hosten lab systems
analog_card = "zotino" # it can be either fastino or zotino for Hosten lab systems
research_group_name = "Hosten"
allow_skipping_images = True
list_of_devices = [
    "core",
    "urukul0_cpld",
    "urukul0_ch0",
    "urukul0_ch1",
    "urukul0_ch2",
    "urukul0_ch3",
    "urukul1_cpld",
    "urukul1_ch0",
    "urukul1_ch1",
    "urukul1_ch2",
    "urukul1_ch3",
    "urukul2_cpld",
    "urukul2_ch0",
    "urukul2_ch1",
    "urukul2_ch2",
    "urukul2_ch3",
    "ttl0",
    "ttl1",
    "ttl2",
    "ttl3",
    "ttl4",
    "ttl5",
    "ttl6",
    "ttl7",
    "ttl8",
    "ttl9",
    "ttl10",
    "ttl11",
    "ttl12",
    "ttl13",
    "ttl14",
    "ttl15",
    "zotino0",
    "sampler0"
]