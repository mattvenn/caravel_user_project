import random
from cocotb.triggers import ClockCycles
import cocotb
from cocotb.queue import Queue
from cocotb.triggers import Combine
from user_design import configure_userdesign
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_monitor_driver import UserPins

@cocotb.test()
@report_test
async def check_defaults(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1145328)
    debug_regs = await configure_userdesign(caravelEnv)
    user_pins = UserPins(caravelEnv)
    gpio_test = GPIOsDefaultTests(caravelEnv, user_pins, debug_regs)
    # read gpios config from file user_define_temp.txt
    user_project_root = cocotb.plusargs["USER_PROJECT_ROOT"].replace('"', "")
    configs = read_config_file(f"{user_project_root}/verilog/rtl/user_define_temp.txt")
    mgmt_out = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_MGMT_STD_OUTPUT")]
    user_out = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_USER_STD_OUTPUT", "GPIO_MODE_USER_STD_OUT_MONITORED")]
    mgmt_in = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_MGMT_STD_INPUT_NOPULL")]
    user_in = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_USER_STD_INPUT_NOPULL")]
    mgmt_in_pu = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_MGMT_STD_INPUT_PULLUP")]
    user_in_pu = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_USER_STD_INPUT_PULLUP")]
    mgmt_in_pd = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_MGMT_STD_INPUT_PULLDOWN")]
    user_in_pd = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_USER_STD_INPUT_PULLDOWN")]
    user_bidirect = [gpio for gpio, type in enumerate(configs) if type in ("GPIO_MODE_USER_STD_BIDIRECTIONAL")]
    user_configs = {"user_in": user_in, "user_in_pu": user_in_pu, "user_in_pd": user_in_pd, "user_out": user_out, "user_bidirect": user_bidirect}
    await ClockCycles(caravelEnv.clk, 10)
    # initialize user oeb and pull up down 
    gpio_test.configure_io_oeb(user_configs)
    gpio_test.configure_pull_up_pd(user_configs)
    # drive all with 1 initialy 
    caravelEnv.drive_gpio_in((37,0), 0x3FFFFFFFFF)
    await ClockCycles(caravelEnv.clk, 1)
    all_out = mgmt_out + user_out
    for gpio in all_out:
        caravelEnv.release_gpio(gpio)
    del all_out
    await ClockCycles(caravelEnv.clk, 1)

    all_modes_tests = []
    # test mgmt_out
    all_modes_tests.append(await cocotb.start(gpio_test.test_mgmt_out(mgmt_out)))

    # test mgmt_in 
    all_modes_tests.append(await cocotb.start(gpio_test.test_mgmt_in(mgmt_in)))

    # test mgmt_in_pu
    all_modes_tests.append(await cocotb.start(gpio_test.test_mgmt_in_pull(mgmt_in_pu, pull_mode="up")))
   
    # # test mgmt_in_pd
    all_modes_tests.append(await cocotb.start(gpio_test.test_mgmt_in_pull(mgmt_in_pd, pull_mode="down")))

    # # test user_out
    all_modes_tests.append(await cocotb.start(gpio_test.test_user_out(user_out)))

    # test user_in
    all_modes_tests.append(await cocotb.start(gpio_test.test_user_in(user_in)))

    # test user_in_pu
    all_modes_tests.append(await cocotb.start(gpio_test.test_user_in_pull(user_in_pu, pull_mode="up")))
    # test user_in_pd
    all_modes_tests.append(await cocotb.start(gpio_test.test_user_in_pull(user_in_pd, pull_mode="pd")))

    # test user_bidirectional
    # all_modes_tests.append(await cocotb.start(test_user_bidirectional(caravelEnv, user_bidirect, user_pins)))

    await Combine(*all_modes_tests)


def read_config_file(filename):
    gpio_configs = []
    with open(filename, 'r') as f:
        for line in f:
            gpio_configs.append(line.strip())
    return gpio_configs


class GPIOsDefaultTests:
    def __init__(self, caravelEnv, user_pins, debug_regs):
        self.caravelEnv = caravelEnv
        self.user_pins = user_pins
        self.debug_regs = debug_regs

    def configure_io_oeb(self, user_configs):
        combined_all_o_eanble = user_configs["user_out"] + user_configs["user_in_pu"] + user_configs["user_in_pd"]
        for i in range(38):
            if i in combined_all_o_eanble:
                self.user_pins.drive_io_oeb(i, 0)
            else:
                self.user_pins.drive_io_oeb(i, 1)

    def configure_pull_up_pd(self, user_configs):
        for i in range(38):
            if i in user_configs["user_in_pu"]:
                self.user_pins.drive_io_out(i, 1)
            elif i in user_configs["user_in_pd"]:
                self.user_pins.drive_io_out(i, 0)

    async def test_user_out(self, gpios):
        cocotb.log.info(f"[TEST] gpios configured as user output = {gpios}")
        queue = Queue()
        await cocotb.start(self.drive_output(queue, gpios))
        for i in range(random.randint(10, 100)):
            data = await queue.get()
            await ClockCycles(self.caravelEnv.clk, 1)
            for index, gpio in enumerate(gpios):
                val = self.caravelEnv.monitor_gpio(gpio).integer
                if val != data[index]:
                    cocotb.log.error(f"[TEST][test_user_out] gpio {gpio} is incorrect expected {data[index]} received {val}")
                else:
                    cocotb.log.debug(f"[TEST][test_user_out] gpio {gpio} is correct received {val}")
        cocotb.log.info(f"[TEST] done with test_user_out")

    async def drive_output(self, queue, gpios):
        while True:
            data = []
            for gpio in gpios:
                random_val = random.randint(0, 1)
                self.user_pins.drive_io_out(gpio, random_val)
                data.append(random_val)
            await queue.put(data)
            await ClockCycles(self.caravelEnv.clk, random.randint(10, 20))


    async def test_user_in(self, gpios):
        cocotb.log.info(f"[TEST] gpios configured as user input = {gpios}")
        for i in range(random.randint(5, 10)):
            await self.caravelEnv.wait_mgmt_gpio(1)
            rand_values = dict()
            for gpio in gpios:
                val = random.randint(0, 1)
                rand_values[gpio] = val
                self.caravelEnv.drive_gpio_in(gpio, val)
            await self.caravelEnv.wait_mgmt_gpio(0)
            for gpio in gpios:
                val = self.user_pins.monitor_io_in(gpio)
                if val != rand_values[gpio]:
                    cocotb.log.error(f"[TEST][test_user_in] gpio {gpio} is not {rand_values[gpio]}")
                else:
                    cocotb.log.debug(f"[TEST][test_user_in] gpio {gpio} is {rand_values[gpio]}")
        cocotb.log.info(f"[TEST] done with test_user_in")

    async def test_user_in_pull(self, gpios, pull_mode="up"):
        cocotb.log.info(f"[TEST] gpios configured as user input pull{pull_mode} = {gpios}")
        for i in range(random.randint(5, 10)):
            await self.caravelEnv.wait_mgmt_gpio(1)
            rand_values = dict()
            for gpio in gpios:
                val = random.choice([1, 0, 'z'])
                rand_values[gpio] = val
                if val == 'z':
                    self.caravelEnv.release_gpio(gpio)
                else:
                    self.caravelEnv.drive_gpio_in(gpio, val)
            await self.caravelEnv.wait_mgmt_gpio(0)
            for gpio in gpios:
                val = self.user_pins.monitor_io_in(gpio)
                rand_val = rand_values[gpio] if rand_values[gpio] != 'z' else 1 if pull_mode == "up" else 0
                if val != rand_val:
                    cocotb.log.error(f"[TEST][test_user_in_pull] pull {pull_mode} gpio {gpio} is not {rand_val} drived by {rand_values[gpio]}")
                else:
                    cocotb.log.debug(f"[TEST][test_user_in_pull] pull {pull_mode} gpio {gpio} is {rand_val} drived by {rand_values[gpio]}")
        cocotb.log.info("[TEST] done with test_user_in_pull")

    async def test_user_bidirectional(self, caravelEnv, gpios):
        cocotb.log.info(f"[TEST] gpios configured as user bidirectional = {gpios}")
        queue = Queue()
        configure_bidirectional = await cocotb.start(self.configure_bidirectional(queue, gpios))
        for i in range(random.randint(10, 100)):
            configurations = await queue.get()
            # release all gpios
            for gpio in gpios:
                caravelEnv.release_gpio(gpio)
            cocotb.log.debug(f"[TEST][test_user_bidirectional] configurations = {configurations}")
            await ClockCycles(caravelEnv.clk, 1)
            # check output
            drived_value = 0 if configurations[0] == "input" else 1
            for index, configuration in enumerate(configurations):
                if configuration == "output":
                    cocotb.log.debug(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is output")
                    val = caravelEnv.monitor_gpio(gpios[index]).integer
                    if val != drived_value:
                        cocotb.log.error(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is incorrect expected {drived_value} received {val}")
                    else:
                        cocotb.log.debug(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is correct received {val}")
            # check input
            rand_values = dict()
            for index, configuration in enumerate(configurations):
                if configuration == "input":
                    cocotb.log.debug(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is input")
                    val = random.randint(0, 1)
                    rand_values[gpios[index]] = val
                    caravelEnv.drive_gpio_in(gpios[index], val)
            await ClockCycles(caravelEnv.clk, 1)
            for index, configuration in enumerate(configurations):
                if configuration == "input":
                    val = self.user_pins.monitor_io_in(gpios[index])
                    rand_val = rand_values[gpios[index]]
                    if val != rand_val:
                        cocotb.log.error(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is not {rand_val} drived by {rand_values[gpios[index]]}")
                    else:
                        cocotb.log.debug(f"[TEST][test_user_bidirectional] gpio {gpios[index]} is {rand_val} drived by {rand_values[gpios[index]]}")
        configure_bidirectional.kill()
        cocotb.log.info("[TEST] done with test_user_bidirectional")

    async def configure_bidirectional(self, queue, gpios):
        while True:
            # configure bidirectional as input or output
            configurations = []
            for gpio in gpios:
                random_val = random.randint(0, 1)
                self.user_pins.drive_io_oeb(gpio, random_val)
                configurations.append("input" if random_val else "output")
            await queue.put(configurations)
            # if first configurations is input drive with 0 else drive with 1
            if configurations[0] == "input":
                for index, gpio in enumerate(gpios):
                    if configurations[index] == "output":
                        cocotb.log.info(f"[TEST] gpio {gpio} configured as output drive with 0")
                        self.user_pins.drive_io_out(gpio, 0)
            else:
                for index, gpio in enumerate(gpios):
                    if configurations[index] == "output":
                        cocotb.log.info(f"[TEST] gpio {gpio} configured as output drive with 1")
                        self.user_pins.drive_io_out(gpio, 1)
            await ClockCycles(self.caravelEnv.clk, random.randint(10, 20))

    async def test_mgmt_out(self, gpios):
        cocotb.log.info(f"[TEST] gpios configured as mgmt output = {gpios}") 
        for i in range(random.randint(5, 10)):
            await self.caravelEnv.wait_mgmt_gpio(1)
            for gpio in gpios:
                val = self.caravelEnv.monitor_gpio(gpio).integer
                if val == 0:
                    cocotb.log.error(f"[TEST][test_mgmt_out] gpio {gpio} is not 1")    
                else: 
                    cocotb.log.debug(f"[TEST][test_mgmt_out] gpio {gpio} is 1")
            await self.caravelEnv.wait_mgmt_gpio(0)
            for gpio in gpios:
                val = self.caravelEnv.monitor_gpio(gpio).integer
                if val == 1:
                    cocotb.log.error(f"[TEST][test_mgmt_out] gpio {gpio} is not 0")
                else: 
                    cocotb.log.debug(f"[TEST][test_mgmt_out] gpio {gpio} is 0")
        cocotb.log.info("[TEST] done with test_mgmt_out")

    async def test_mgmt_in(self, gpios):
        cocotb.log.info(f"[TEST] gpios configured as mgmt input = {gpios}")
        for i in range(random.randint(5, 10)):
            await self.caravelEnv.wait_mgmt_gpio(1)
            rand_values = dict()
            for gpio in gpios:
                val = random.randint(0, 1)
                rand_values[gpio] = val
                self.caravelEnv.drive_gpio_in(gpio, val)
            await self.caravelEnv.wait_mgmt_gpio(0)
            gpio_high_reg = self.debug_regs.read_debug_reg2()
            gpio_low_reg = self.debug_regs.read_debug_reg1()
            for gpio in gpios:
                if gpio < 32:
                    val = self.get_bit_from_reg(gpio_low_reg, gpio)
                    if val != rand_values[gpio]:
                        cocotb.log.error(f"[TEST][test_mgmt_in] gpio {gpio} is not {rand_values[gpio]}")
                    else:
                        cocotb.log.debug(f"[TEST][test_mgmt_in] gpio {gpio} is {rand_values[gpio]}")
                else:
                    val = self.get_bit_from_reg(gpio_high_reg, gpio-32)
                    if val != rand_values[gpio]:
                        cocotb.log.error(f"[TEST][test_mgmt_in] gpio {gpio} is not {rand_values[gpio]}")
                    else:
                        cocotb.log.debug(f"[TEST][test_mgmt_in] gpio {gpio} is {rand_values[gpio]}")   
        cocotb.log.info("[TEST] done with test_mgmt_in")

    async def test_mgmt_in_pull(self, gpios, pull_mode="up"):
        cocotb.log.info(f"[TEST] gpios configured as mgmt input pull{pull_mode} = {gpios}")
        for i in range(random.randint(5, 10)):
            await self.caravelEnv.wait_mgmt_gpio(1)
            rand_values = dict()
            for gpio in gpios:
                val = random.choice([1, 0, 'z'])
                rand_values[gpio] = val
                if val == 'z':
                    self.caravelEnv.release_gpio(gpio)
                else:
                    self.caravelEnv.drive_gpio_in(gpio, val)
            await self.caravelEnv.wait_mgmt_gpio(0)
            gpio_high_reg = self.debug_regs.read_debug_reg2()
            gpio_low_reg = self.debug_regs.read_debug_reg1()
            for gpio in gpios:
                rand_val = rand_values[gpio] if rand_values[gpio] != 'z' else 1 if pull_mode == "up" else 0
                if gpio < 32:
                    val = self.get_bit_from_reg(gpio_low_reg, gpio)
                    if val != rand_val:
                        cocotb.log.error(f"[TEST][test_mgmt_in_pull] pull {pull_mode} gpio {gpio} is not {rand_values[gpio]}")
                    else:
                        cocotb.log.debug(f"[TEST][test_mgmt_in_pull] pull {pull_mode} gpio {gpio} is {rand_values[gpio]}")
                else:
                    val = self.get_bit_from_reg(gpio_high_reg, gpio-32)
                    if val != rand_val:
                        cocotb.log.error(f"[TEST][test_mgmt_in_pull] pull {pull_mode} gpio {gpio} is not {rand_val} drived by {rand_values[gpio]}")
                    else:
                        cocotb.log.debug(f"[TEST][test_mgmt_in_pull] pull {pull_mode} gpio {gpio} is {rand_val} drived by {rand_values[gpio]}")
        cocotb.log.info("[TEST] done with test_mgmt_in_pull")

    def get_bit_from_reg(self, reg, gpio):
        return (reg & (1 << gpio)) >> gpio
