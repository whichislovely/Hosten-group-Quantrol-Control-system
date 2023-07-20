from artiq.experiment import *


class LED(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("led0")

    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        for i in range(10):
            self.led0.on()
            delay(0.5*s)
            self.led0.off()
            delay(0.5*s)


