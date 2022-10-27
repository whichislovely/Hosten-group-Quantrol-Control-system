# Kasli v1.1 SN 29

# Notes:
# * The EEMs are connected to be compatible with the
#   artiq-kasli-ist bitstreams. Those bitstreams can be
#   used without modification with the device_db.py below.
# * The JSON configuration for the bitstream is located at
#   https://github.com/m-labs/sinara-systems and can be built using the ARTIQ
#   generic Kasli target (python -m artiq.gateware.targets.kasli_generic
#   <system-name>.json).
# * The binary packages with the bitstreams are available at the M-Labs Hydra
#   buildbot: https://nixbld.m-labs.hk/jobset/artiq/sinara-systems
# * A script to create a custom Conda environment is available at:
#   https://github.com/m-labs/artiq/blob/master/conda/install-artiq.py
#   It requires editing to adapt to the specific variant.
# * DIO_BNC TTL channels (none) are configured ad inputs on the EEM and
#   TTLInOut in the gateware. The remaining digital channels are Outputs
#   on the EEM and in the gateware.
# * MMCX cables to connect the Kasli 125 MHz outputs to the
#   Urukul reference input or to connect Clocker to Kasli and/or to Urukul
#   are included.
# * Kasli is configured to use the IP below. That can be changed using
#   artiq_coremgmt or artiq_mkfs+artiq_flash.

# # Sinara
#
# The Sinara components are open hardware. The designs are available under the
# terms of the CERN Open Hardware License v1.2
# (https://www.ohwr.org/attachments/2390/cern_ohl_v_1_2.pdf) at:
# https://github.com/sinara-hw/sinara
#
# # ARTIQ
#
# ARTIQ is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# ARTIQ is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with ARTIQ. If not, see <http://www.gnu.org/licenses/>.
#
# The ARTIQ source code is available at https://github.com/m-labs/artiq
#
# # Electrical
#
# Modification and disassembly of the crate must only be done with proper ESD
# protection and with the devices disconnected. Modifications that go beyond the
# manipulation of the DIP switches or addition/removal of modules by qualified
# personnel will void the warranty.
#
# The controller and the modules are electrically floating and not connected
# to mains ground via the power supply. A proper ground connection should be
# established at an appropriate place.
# As with any class II supply without ground connection there is a capacitive
# coupling between mains voltage and ground output. Ensure that this voltage
# is shunted by properly gorunding the device.
#
# # Thermal
#
# The crate needs unrestricted airflow for cooling. Keep the bottom and top
# surfaces clear. In a rack leave 1U below and 1U above unused or use a [fan](
# https://www.reichelt.de/Zubehoer-Schaltschrankgehaeuse/LOGILINK-FAU02FG/3/index.html?ARTICLE=161905)
# [tray](https://www.digikey.de/product-detail/en/orion-fans/OA300ST-230/1053-1428-ND/2658718).
#
# # Network
#
# The system is shipped with a RJ45 SFP module or a pair of BiDi SFP modules
# ([1000Base-BX-U](https://www.fs.com/products/11802.html) and
# [1000Base-BX-D](https://www.fs.com/products/11795.html)) and a fiber.
# Removal of SFP modules from their slots is achieved by flipping the wire
# handle and pulling lightly.
# The SFP transcievers are known to work in several switches (e.g. [Netgear
# GS110TP](https://www.netgear.com/support/product/GS110TP.aspx)) or media
# converters (e.g. [TP-Link
# MC220L](https://www.tp-link.com/us/products/details/cat-43_MC220L.html)).
# Connect the blue SFP module in Kasli and the violet module in the switch with
# the simplex fiber.
#
# Ensure that your switch or media converter supports "generic" (i.e. not same
# vendor) SFP modules with 1000Base-X (no auto negotiation) mode. Some switch
# vendors are picky with regards to the SFP module vendors.
#
# Alternatively, obtain different SFP modules (e.g. a pair of 1000Base-LX or
# 1000Base-SX and a duplex fiber, a direct attach cable, or a RJ45 1000Base-T
# GBIC) that fit your infrastructure.

core_addr = "10.0.16.129"



device_db = {
    "core": {
        "type": "local",
        "module": "artiq.coredevice.core",
        "class": "Core",
        "arguments": {"host": core_addr, "ref_period": 1e-9}
    },
    "core_log": {
        "type": "controller",
        "host": "::1",
        "port": 1068,
        "command": "aqctl_corelog -p {port} --bind {bind} " + core_addr
    },
    "core_cache": {
        "type": "local",
        "module": "artiq.coredevice.cache",
        "class": "CoreCache"
    },
    "core_dma": {
        "type": "local",
        "module": "artiq.coredevice.dma",
        "class": "CoreDMA"
    },

    "i2c_switch0": {
        "type": "local",
        "module": "artiq.coredevice.i2c",
        "class": "PCA9548",
        "arguments": {"address": 0xe0}
    },
    "i2c_switch1": {
        "type": "local",
        "module": "artiq.coredevice.i2c",
        "class": "PCA9548",
        "arguments": {"address": 0xe2}
    },
}


device_db.update({
    "ttl" + str(i): {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLInOut" if i < 0 else "TTLOut",
        "arguments": {"channel": i},
    } for i in range(32)
})


for j in range(3):
    device_db.update({
        "spi_urukul{}".format(j): {
            "type": "local",
            "module": "artiq.coredevice.spi2",
            "class": "SPIMaster",
            "arguments": {"channel": 32 + 7*j}
        },
        "ttl_urukul{}_sync".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLClockGen",
            "arguments": {"channel": 32 + 7*j + 1, "acc_width": 4}
        },
        "ttl_urukul{}_io_update".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLOut",
            "arguments": {"channel": 32 + 7*j + 2}
        },
        "ttl_urukul{}_sw0".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLOut",
            "arguments": {"channel": 32 + 7*j + 3}
        },
        "ttl_urukul{}_sw1".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLOut",
            "arguments": {"channel": 32 + 7*j + 4}
        },
        "ttl_urukul{}_sw2".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLOut",
            "arguments": {"channel": 32 + 7*j + 5}
        },
        "ttl_urukul{}_sw3".format(j): {
            "type": "local",
            "module": "artiq.coredevice.ttl",
            "class": "TTLOut",
            "arguments": {"channel": 32 + 7*j + 6}
        },
        "urukul{}_cpld".format(j): {
            "type": "local",
            "module": "artiq.coredevice.urukul",
            "class": "CPLD",
            "arguments": {
                "spi_device": "spi_urukul{}".format(j),
                "io_update_device": "ttl_urukul{}_io_update".format(j),
                "sync_device": "ttl_urukul{}_sync".format(j),
                "clk_sel": 1,
                "refclk": 1e9,
                "clk_div": 1,
            }
        }
    })

    device_db.update({
        "urukul{}_ch{}".format(j, i): {
            "type": "local",
            "module": "artiq.coredevice.ad9910",
            "class": "AD9910",
            "arguments": {
                "pll_en": 0,
                "chip_select": 4 + i,
                "cpld_device": "urukul{}_cpld".format(j),
                "sw_device": "ttl_urukul{}_sw{}".format(j, i)
            }
        } for i in range(4)
    })


device_db.update({
    "spi_sampler0_adc": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 53}
    },
    "spi_sampler0_pgia": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 54}
    },
    "spi_sampler0_cnv": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 55},
    },
    "sampler0": {
        "type": "local",
        "module": "artiq.coredevice.sampler",
        "class": "Sampler",
        "arguments": {
            "spi_adc_device": "spi_sampler0_adc",
            "spi_pgia_device": "spi_sampler0_pgia",
            "cnv_device": "spi_sampler0_cnv"
        }
    }
})


device_db.update({
    "spi_zotino0": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 56}
    },
    "ttl_zotino0_ldac": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 57}
    },
    "ttl_zotino0_clr": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 58}
    },
    "zotino0": {
        "type": "local",
        "module": "artiq.coredevice.zotino",
        "class": "Zotino",
        "arguments": {
            "spi_device": "spi_zotino0",
            "ldac_device": "ttl_zotino0_ldac",
            "clr_device": "ttl_zotino0_clr"
        }
    }
})


device_db.update({
    "led0": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 59}
    },
    "led1": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 60}
    }
})
