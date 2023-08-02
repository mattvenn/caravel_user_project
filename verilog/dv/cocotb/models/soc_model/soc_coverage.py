from cocotb_coverage.coverage import CoverPoint, CoverCross
from collections import namedtuple
import cocotb

class UART_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.uart_cov(None, do_sampling=False)

    def uart_cov(self, operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.soc.uart.type",
            xf=lambda operation: operation.type,
            bins=["rx", "tx"]
        )
        @CoverPoint(
            "top.caravel.soc.uart.char",
            xf=lambda operation: ord(operation.char),
            bins=[(0x0, 0x10), (0x10, 0x20), (0x20, 0x30), (0x30, 0x40), (0x40, 0x50), (0x50, 0x60), (0x60, 0x70), (0x70, 0x80)],
            bins_labels=["0 to 0x10", "0x10 to 0x20", "0x20 to 0x30", "0x30 to 0x40", "0x40 to 0x50", "0x50 to 0x60", "0x60 to 0x70", "0x70 to 0x80"],
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverCross(
            "top.caravel.soc.uart.char_type",
            items=[
                "top.caravel.soc.uart.char",
                "top.caravel.soc.uart.type",
            ],
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)


class MSPI_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.spi_cov(None, do_sampling=False)

    def spi_cov(self, operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.soc.master_spi.spi_write_byte",
            xf=lambda operation: int(operation.data_write, 2),
            bins=[(0, 0x0F), (0x10, 0x1F), (0x20, 0x2F), (0x30, 0x3F), (0x40, 0x4F), (0x50, 0x5F), (0x60, 0x6F), (0x70, 0x7F), (0x80, 0x8F), (0x90, 0x9F), (0xA0, 0xAF), (0xB0, 0xBF), (0xC0, 0xCF), (0xD0, 0xDF), (0xE0, 0xEF), (0xF0, 0xFF)],
            bins_labels=["0x0, 0x0F", "0x10, 0x1F", "0x20, 0x2F", "0x30, 0x3F", "0x40, 0x4F", "0x50, 0x5F", "0x60, 0x6F", "0x70, 0x7F", "0x80, 0x8F", "0x90, 0x9F", "0xA0, 0xAF", "0xB0, 0xBF", "0xC0, 0xCF", "0xD0, 0xDF", "0xE0, 0xEF", "0xF0, 0xFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        @CoverPoint(
            "top.caravel.soc.master_spi.spi_read_byte",
            xf=lambda operation: int(operation.data_read, 2),
            bins=[(0, 0x0F), (0x10, 0x1F), (0x20, 0x2F), (0x30, 0x3F), (0x40, 0x4F), (0x50, 0x5F), (0x60, 0x6F), (0x70, 0x7F), (0x80, 0x8F), (0x90, 0x9F), (0xA0, 0xAF), (0xB0, 0xBF), (0xC0, 0xCF), (0xD0, 0xDF), (0xE0, 0xEF), (0xF0, 0xFF)],
            bins_labels=["0x0, 0x0F", "0x10, 0x1F", "0x20, 0x2F", "0x30, 0x3F", "0x40, 0x4F", "0x50, 0x5F", "0x60, 0x6F", "0x70, 0x7F", "0x80, 0x8F", "0x90, 0x9F", "0xA0, 0xAF", "0xB0, 0xBF", "0xC0, 0xCF", "0xD0, 0xDF", "0xE0, 0xEF", "0xF0, 0xFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)


class Debug_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.debug_cov(None, do_sampling=False)

    def debug_cov(self, operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.soc.debug_if.type",
            xf=lambda operation: operation.type,
            bins=["rx", "tx"]
        )
        @CoverPoint(
            "top.caravel.soc.debug_if.values",
            xf=lambda operation: int(operation.char, 16),
            bins=[(0x0, 0x0F)],
            bins_labels=["0x0, 0x0F"],
            rel=lambda val, b: b[0] <= val <= b[1],
            at_least=5
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)


class IRQ_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.irq_cov(None, do_sampling=False)
        pass

    def irq_cov(self, data, do_sampling=True):
        @CoverPoint(
            "top.caravel.soc.irq.timer",
            xf=lambda data: data,
            bins=[("timer_interrupt", "clear"), ("timer_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.uart",
            xf=lambda data: data,
            bins=[("uart_interrupt", "clear"), ("uart_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.user0",
            xf=lambda data: data,
            bins=[("user0_interrupt", "clear"), ("user0_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.user1",
            xf=lambda data: data,
            bins=[("user1_interrupt", "clear"), ("user1_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.user2",
            xf=lambda data: data,
            bins=[("user2_interrupt", "clear"), ("user2_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.housekeeping",
            xf=lambda data: data,
            bins=[("housekeeping_interrupt", "clear"), ("housekeeping_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"]
        )
        @CoverPoint(
            "top.caravel.soc.irq.external1",
            xf=lambda data: data,
            bins=[("external1_interrupt", "clear"), ("external1_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"],
        )
        @CoverPoint(
            "top.caravel.soc.irq.external2",
            xf=lambda data: data,
            bins=[("external2_interrupt", "clear"), ("external2_interrupt", "interrupt")],
            rel=lambda data, b: data[0] == b[0] and data[1] == b[1],
            bins_labels=["clear", "interrupt"],
        )
        def sample(data):
            pass
        if do_sampling:
            sample(data)
        

