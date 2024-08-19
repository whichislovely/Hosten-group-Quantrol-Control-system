from artiq.experiment import *

class init_hardware(EnvExperiment):
    def build(self):
        self.setattr_device('core')
        self.setattr_device('urukul0_cpld')
        self.setattr_device('urukul0_ch0')
        self.setattr_device('urukul0_ch1')
        self.setattr_device('urukul0_ch2')
        self.setattr_device('urukul0_ch3')
        self.setattr_device('urukul1_cpld')
        self.setattr_device('urukul1_ch0')
        self.setattr_device('urukul1_ch1')
        self.setattr_device('urukul1_ch2')
        self.setattr_device('urukul1_ch3')
        self.setattr_device('urukul2_cpld')
        self.setattr_device('urukul2_ch0')
        self.setattr_device('urukul2_ch1')
        self.setattr_device('urukul2_ch2')
        self.setattr_device('urukul2_ch3')
        self.setattr_device('ttl0')
        self.setattr_device('ttl1')
        self.setattr_device('ttl2')
        self.setattr_device('ttl3')
        self.setattr_device('ttl4')
        self.setattr_device('ttl5')
        self.setattr_device('ttl6')
        self.setattr_device('ttl7')
        self.setattr_device('ttl8')
        self.setattr_device('ttl9')
        self.setattr_device('ttl10')
        self.setattr_device('ttl11')
        self.setattr_device('ttl12')
        self.setattr_device('ttl13')
        self.setattr_device('ttl14')
        self.setattr_device('ttl15')
        self.setattr_device('fastino0')

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        delay(5*ms)
        delay(5*ms)
        self.ttl0.off()
        self.ttl1.off()
        self.ttl2.off()
        self.ttl3.off()
        self.ttl4.off()
        self.ttl5.off()
        self.ttl6.off()
        self.ttl7.off()
        delay(5*ms)
        self.ttl8.off()
        self.ttl9.off()
        self.ttl10.off()
        self.ttl11.off()
        self.ttl12.off()
        self.ttl13.off()
        self.ttl14.off()
        self.ttl15.off()
        delay(10*ns)
        delay(10*ns)
        self.fastino0.set_dac(0, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(1, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(2, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(3, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(4, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(5, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(6, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(7, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(8, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(9, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(10, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(11, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(12, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(13, -9.000000)
        delay(10*ns)
        self.fastino0.set_dac(14, 9.000000)
        delay(10*ns)
        self.fastino0.set_dac(15, -9.000000)
        self.urukul0_ch0.set_att(0.0*dB) 
        self.urukul0_ch0.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul0_ch0.sw.off() 
        self.urukul0_ch1.set_att(0.0*dB) 
        self.urukul0_ch1.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul0_ch1.sw.off() 
        self.urukul0_ch2.set_att(0.0*dB) 
        self.urukul0_ch2.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul0_ch2.sw.off() 
        self.urukul0_ch3.set_att(0.0*dB) 
        self.urukul0_ch3.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul0_ch3.sw.off() 
        self.urukul1_ch0.set_att(0.0*dB) 
        self.urukul1_ch0.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul1_ch0.sw.off() 
        self.urukul1_ch1.set_att(0.0*dB) 
        self.urukul1_ch1.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul1_ch1.sw.off() 
        self.urukul1_ch2.set_att(0.0*dB) 
        self.urukul1_ch2.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul1_ch2.sw.off() 
        self.urukul1_ch3.set_att(0.0*dB) 
        self.urukul1_ch3.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul1_ch3.sw.off() 
        self.urukul2_ch0.set_att(0.0*dB) 
        self.urukul2_ch0.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul2_ch0.sw.off() 
        self.urukul2_ch1.set_att(0.0*dB) 
        self.urukul2_ch1.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul2_ch1.sw.off() 
        self.urukul2_ch2.set_att(0.0*dB) 
        self.urukul2_ch2.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul2_ch2.sw.off() 
        self.urukul2_ch3.set_att(0.0*dB) 
        self.urukul2_ch3.set(frequency = 0.0*MHz, amplitude = 0.0, phase = (0.0)/360)
        self.urukul2_ch3.sw.off() 
