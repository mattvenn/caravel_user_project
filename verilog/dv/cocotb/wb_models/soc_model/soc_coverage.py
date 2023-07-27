from cocotb_coverage.coverage import CoverPoint, CoverCross
from collections import namedtuple


class UART_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        temp = namedtuple('temp', ['type', 'char'])

        self.uart_cov(temp(type="cc", char=" "))

    def uart_cov(self, operation):
        @CoverPoint(
            "top.caravel.soc.uart.type",
            xf=lambda operation: operation.type,
            bins=["rx", "tx"],
            weight=1
        )
        @CoverPoint(
            "top.caravel.soc.uart.char",
            xf=lambda operation: ord(operation.char),
            bins=[(0x0, 0x10), (0x10, 0x20), (0x20, 0x30), (0x30, 0x40), (0x40, 0x50), (0x50, 0x60), (0x60, 0x70), (0x70, 0x80)],
            bins_labels=["0 to 0x10", "0x10 to 0x20", "0x20 to 0x30", "0x30 to 0x40", "0x40 to 0x50", "0x50 to 0x60", "0x60 to 0x70", "0x70 to 0x80"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
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
        sample(operation)
