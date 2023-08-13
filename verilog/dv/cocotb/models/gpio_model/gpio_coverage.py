from cocotb_coverage.coverage import CoverPoint, CoverCross, CoverageDB
import cocotb


class GPIOs_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.gpios_cov = dict()
        for gpio_num in range(38):
            for ty in ["configured", "default"]:
                self.gpios_cov[(gpio_num, ty)] = GPIO_coverage(gpio_num, ty)

    def gpio_cov(self, operation, do_sampling=True):
        gpio_num = operation.gpio_number
        ty = operation.config_type
        self.gpios_cov[(gpio_num, ty)].gpio_config_cov(operation, do_sampling)
    
    def io_cov(self, operation, do_sampling=True):
        gpio_num = operation.gpio_number
        ty = "configured"
        self.gpios_cov[(gpio_num, ty)].gpio_io_cov(operation, do_sampling)


class GPIO_coverage():
    def __init__(self, gpio_number, config_type) -> None:
        self.gpio_number = gpio_number
        self.config_type = config_type
        self.control_list = ["user", "managment"]
        self.input_list = ["input enabled", "input disabled"]
        self.output_list = ["output enabled", "output disabled"]
        self.dm_list = ["no pull", "pull up", "pull down", "float", "analog"]
        self.config_valid_ignore = [(i, j, "input disabled", k) for i in self.control_list for j in self.output_list for k in ['pull down', 'pull up']] + [(i, 'output disabled', 'input enabled', j) for i in self.control_list for j in ["pull down", "pull up"]] + [(i, j, 'input disabled', "no pull") for i in self.control_list for j in self.output_list] + [(i, 'output enabled', 'input enabled', 'no pull') for i in self.control_list] + [(i, 'output disabled', j, 'float') for i in self.control_list for j in self.input_list] + [(i, 'output enabled', j, 'analog') for i in self.control_list for j in self.input_list] + [(i, j, "input enabled", 'analog') for i in self.control_list for j in self.output_list] + [('managment', 'output enabled', 'input enabled', 'float')]
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.gpio_config_cov(None, do_sampling=False)
        self.gpio_io_cov(None, do_sampling=False)

    def gpio_io_cov(self, operation, do_sampling=True):
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.IO.managment",
            xf=lambda operation: operation,
            bins=[("mgmt", "input", "0"), ("mgmt", "input", "1"), ("mgmt", "output", "0"), ("mgmt", "output", "1")],
            bins_labels=[ "input 0", "input 1", "output 0", "output 1"],
            rel=lambda val, b: val.control == b[0] and val.io == b[1] and val.value == b[2]
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.IO.user",
            xf=lambda operation: operation,
            bins=[("user", "input", "0"), ("user", "input", "1"), ("user", "output", "0"), ("user", "output", "1")],
            bins_labels=["input 0", "input 1", "output 0", "output 1"],
            rel=lambda val, b: val.control == b[0] and val.io == b[1] and val.value == b[2]
        )
        @CoverCross(
            f"top.caravel.gpios.GPIO{self.gpio_number}.IO.in_out_user_configs",
            items=[
                f"top.caravel.gpios.GPIO{self.gpio_number}.IO.user",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.controlled_by",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.output",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.input",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.dm"
            ],
            ign_bins=[(i, valid[0], valid[1], valid[2], valid[3]) for i in ["input 0", "input 1", "output 0", "output 1"] for valid in self.config_valid_ignore] + [(i, 'managment', j, k, l) for i in ["input 0", "input 1", "output 0", "output 1"] for j in self.output_list for k in self.input_list for l in self.dm_list]  + [(i,'user', j, 'input disabled', k) for i in ["input 0", "input 1"] for j in self.output_list for k in self.dm_list if k != "analog"] + [(i, 'user', 'output disabled', j,  k) for i in ["output 0", "output 1"] for j in self.input_list for k in self.dm_list if k != "analog"] + [(i, 'user', j, k, l) for i in ["output 0", "output 1"] for j in self.output_list for k in self.input_list for l in ["pull down", "pull up", "no pull"]]
        )
        @CoverCross(
            f"top.caravel.gpios.GPIO{self.gpio_number}.IO.in_out_mgmt_configs",
            items=[
                f"top.caravel.gpios.GPIO{self.gpio_number}.IO.managment",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.controlled_by",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.output",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.input",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.dm"
            ],
            ign_bins=[(i, valid[0], valid[1], valid[2], valid[3]) for i in ["input 0", "input 1", "output 0", "output 1"] for valid in self.config_valid_ignore] + [(i, 'user', j, k, l) for i in ["input 0", "input 1", "output 0", "output 1"] for j in self.output_list for k in self.input_list for l in self.dm_list]  + [(i,'managment', j, 'input disabled', k) for i in ["input 0", "input 1"] for j in self.output_list for k in self.dm_list if k != "analog"] + [(i, 'managment', 'output disabled', j,  k) for i in ["output 0", "output 1"] for j in self.input_list for k in self.dm_list if k != "analog"] + [(i, 'managment', j, k, l) for i in ["output 0", "output 1"] for j in self.output_list for k in self.input_list for l in ["pull down", "pull up", "no pull"]]
        )
        def sample(operation):
            # if self.gpio_number == 0:
                # cocotb.log.info(f"[COV] io_user = {CoverageDB()[f'top.caravel.gpios.GPIO{self.gpio_number}.IO.user'].detailed_coverage}")
                # cocotb.log.info(f"[COV] valid = {CoverageDB()[f'top.caravel.gpios.GPIO{self.gpio_number}.configured.valid_configs'].detailed_coverage}")
            pass
        if do_sampling:
            sample(operation)
    def gpio_config_cov(self, operation, do_sampling=True):
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.controlled_by",
            xf=lambda operation: operation.mgmt_en,
            bins=[0, 1],
            bins_labels=self.control_list,
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.output",
            xf=lambda operation: operation.outenb,
            bins=[0, 1],
            bins_labels=self.output_list,
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.input",
            xf=lambda operation: operation.inenb,
            bins=[0, 1],
            bins_labels=self.input_list,
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.dm",
            xf=lambda operation: operation.dm,
            bins=[0x1, 0x2, 0x3, 0x6, 0x0],
            bins_labels=self.dm_list
        )
        @CoverCross(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.valid_configs",
            items=[
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.controlled_by",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.output",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.input",
                f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.dm",
            ],
            ign_bins=self.config_valid_ignore
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.hold_override_val",
            xf=lambda operation: operation.holdover,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.IB_mode_select",
            xf=lambda operation: operation.ib_sel,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.analog_bus_en",
            xf=lambda operation: operation.ana_en,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.analog_bus_select",
            xf=lambda operation: operation.ana_sel,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.analog_bus_polarity",
            xf=lambda operation: operation.ana_pol,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.slow_slew",
            xf=lambda operation: operation.slow_selw,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        @CoverPoint(
            f"top.caravel.gpios.GPIO{self.gpio_number}.{self.config_type}.voltage_trip_select",
            xf=lambda operation: operation.vtrip,
            bins=[0x0], # TODO: update it when the bit functionality is implemented
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)