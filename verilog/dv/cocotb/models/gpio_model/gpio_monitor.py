import cocotb
from cocotb.triggers import RisingEdge
from collections import namedtuple

GPIO_Config = namedtuple("GPIO_Config", ["gpio_number", "config_type", "mgmt_en", "outenb", "holdover", "inenb", "ib_sel", "ana_en", "ana_sel", "ana_pol", "slow_selw", "vtrip", "dm"])


class GPIOs_Monitor():
    def __init__(self, Caravel_env, config_queue):
        self.caravel_hdl = Caravel_env.caravel_hdl
        self.config_queue = config_queue
        self.gpio_mapping = {
            0:  "gpio_control_bidir_1[0]",
            1:  "gpio_control_bidir_1[1]",
            2:  "gpio_control_in_1a[0]",
            3:  "gpio_control_in_1a[1]",
            4:  "gpio_control_in_1a[2]",
            5:  "gpio_control_in_1a[3]",
            6:  "gpio_control_in_1a[4]",
            7:  "gpio_control_in_1a[5]",
            8:  "gpio_control_in_1[0]",
            9:  "gpio_control_in_1[1]",
            10: "gpio_control_in_1[2]",
            11: "gpio_control_in_1[3]",
            12: "gpio_control_in_1[4]",
            13: "gpio_control_in_1[5]",
            14: "gpio_control_in_1[6]",
            15: "gpio_control_in_1[7]",
            16: "gpio_control_in_1[8]",
            17: "gpio_control_in_1[9]",
            18: "gpio_control_in_1[10]",
            19: "gpio_control_in_2[0]",
            20: "gpio_control_in_2[1]",
            21: "gpio_control_in_2[2]",
            22: "gpio_control_in_2[3]",
            23: "gpio_control_in_2[4]",
            24: "gpio_control_in_2[5]",
            25: "gpio_control_in_2[6]",
            26: "gpio_control_in_2[7]",
            27: "gpio_control_in_2[8]",
            28: "gpio_control_in_2[9]",
            29: "gpio_control_in_2[10]",
            30: "gpio_control_in_2[11]",
            31: "gpio_control_in_2[12]",
            32: "gpio_control_in_2[13]",
            33: "gpio_control_in_2[14]",
            34: "gpio_control_in_2[15]",
            35: "gpio_control_bidir_2[0]",
            36: "gpio_control_bidir_2[1]",
            37: "gpio_control_bidir_2[2]"}
        self._config_monitor()

    def _config_monitor(self):
        for key, item in self.gpio_mapping.items():
            gpio_hdl = self.caravel_hdl._id(item, False)
            GPIO_Monitor(queue=self.config_queue, gpio_hdl=gpio_hdl, gpio_num=key)


class GPIO_Monitor():
    def __init__(self, queue, gpio_hdl, gpio_num) -> None:
        self.gpio_hdl = gpio_hdl
        self.gpio_num = gpio_num
        self._config_fork = cocotb.scheduler.add(self._config_monitor(queue))

    async def _config_monitor(self, queue):
        self._control_block_hdls()
        config = GPIO_Config(gpio_number=self.gpio_num, config_type="default", mgmt_en=self.mgmt_ena.value.integer, outenb=self.gpio_outenb.value.integer, holdover=self.gpio_holdover.value.integer, inenb=self.gpio_inenb.value.integer, ib_sel=self.gpio_ib_mode_sel.value.integer, ana_en=self.gpio_ana_en.value.integer, ana_sel=self.gpio_ana_sel.value.integer, ana_pol=self.gpio_ana_pol.value.integer, slow_selw=self.gpio_slow_sel.value.integer, vtrip=self.gpio_vtrip_sel.value.integer, dm=self.gpio_dm.value.integer)
        queue.put_nowait(config)
        cocotb.log.info(f"[{__class__.__name__}][_config_monitor] sending config {config} to queue")
        while True:
            await RisingEdge(self.serial_load)
            config = GPIO_Config(gpio_number=self.gpio_num, config_type="configured", mgmt_en=self.mgmt_ena.value.integer, outenb=self.gpio_outenb.value.integer, holdover=self.gpio_holdover.value.integer, inenb=self.gpio_inenb.value.integer, ib_sel=self.gpio_ib_mode_sel.value.integer, ana_en=self.gpio_ana_en.value.integer, ana_sel=self.gpio_ana_sel.value.integer, ana_pol=self.gpio_ana_pol.value.integer, slow_selw=self.gpio_slow_sel.value.integer, vtrip=self.gpio_vtrip_sel.value.integer, dm=self.gpio_dm.value.integer)
            queue.put_nowait(config)
            cocotb.log.info(f"[{__class__.__name__}][_config_monitor] sending config {config} to queue")

    def _control_block_hdls(self):
        self.mgmt_ena = self.gpio_hdl.mgmt_ena
        self.gpio_holdover = self.gpio_hdl.gpio_holdover
        self.gpio_slow_sel = self.gpio_hdl.gpio_slow_sel
        self.gpio_vtrip_sel = self.gpio_hdl.gpio_vtrip_sel
        self.gpio_ib_mode_sel = self.gpio_hdl.gpio_ib_mode_sel
        self.gpio_inenb = self.gpio_hdl.gpio_inenb
        self.gpio_outenb = self.gpio_hdl.gpio_outenb
        self.gpio_dm = self.gpio_hdl.gpio_dm
        self.gpio_ana_en = self.gpio_hdl.gpio_ana_en
        self.gpio_ana_sel = self.gpio_hdl.gpio_ana_sel
        self.gpio_ana_pol = self.gpio_hdl.gpio_ana_pol
        self.serial_load = self.gpio_hdl.serial_load

