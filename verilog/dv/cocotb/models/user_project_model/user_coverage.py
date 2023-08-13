from cocotb_coverage.coverage import CoverPoint, CoverCross


class WB_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.wb_cov(None, do_sampling=False)

    def wb_cov(self, wb_operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.user.wishbone.access_type",
            xf=lambda wb_operation: wb_operation.write,
            bins=[0, 1],
            bins_labels=["read", "write"],
            weight=1
        )
        @CoverPoint(
            "top.caravel.user.wishbone.address",
            xf=lambda wb_operation: wb_operation.address,
            bins=[(0x30000000, 0x30020000), (0x30020001, 0x30040000), (0x30040001, 0x30060000), (0x30060001, 0x30080000), (0x30080001, 0x300A0000), (0x300A0001, 0x300C0000), (0x300C0001, 0x300E0000), (0x300E0001, 0x30100000)],
            bins_labels=["0x30000000 to 0x30020000", "0x30020001 to 0x30040000", "0x30040001 to 0x30060000", "0x30060001 to 0x30080000", "0x30080001 to 0x300A0000", "0x300A0001 to 0x300C0000", "0x300C0001 to 0x300E0000", "0x300E0001 to 0x30100000"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
        )
        @CoverPoint(
            "top.caravel.user.wishbone.write_data",
            xf=lambda wb_operation: wb_operation.write_data,
            bins=[(0x00000000, 0x1FFFFFFF), (0x20000000, 0x3FFFFFFF), (0x40000000, 0x5FFFFFFF), (0x60000000, 0x7FFFFFFF), (0x80000000, 0x9FFFFFFF), (0xA0000000, 0xBFFFFFFF), (0xC0000000, 0xDFFFFFFF), (0xE0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x1FFFFFFF", "0x20000000 to 0x3FFFFFFF", "0x40000000 to 0x5FFFFFFF", "0x60000000 to 0x7FFFFFFF", "0x80000000 to 0x9FFFFFFF", "0xA0000000 to 0xBFFFFFFF", "0xC0000000 to 0xDFFFFFFF", "0xE0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        @CoverPoint(
            "top.caravel.user.wishbone.read_data",
            xf=lambda wb_operation: wb_operation.read_data,
            bins=[(0x00000000, 0x1FFFFFFF), (0x20000000, 0x3FFFFFFF), (0x40000000, 0x5FFFFFFF), (0x60000000, 0x7FFFFFFF), (0x80000000, 0x9FFFFFFF), (0xA0000000, 0xBFFFFFFF), (0xC0000000, 0xDFFFFFFF), (0xE0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x1FFFFFFF", "0x20000000 to 0x3FFFFFFF", "0x40000000 to 0x5FFFFFFF", "0x60000000 to 0x7FFFFFFF", "0x80000000 to 0x9FFFFFFF", "0xA0000000 to 0xBFFFFFFF", "0xC0000000 to 0xDFFFFFFF", "0xE0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample(wb_operation):
            pass
        if do_sampling:
            sample(wb_operation)

class LA_Coverage():
    def __init__(self, la_number) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.la_number = la_number
        self.bits_cov = dict()
        for i in range(la_number):
            self.bits_cov[i] = LA_Bit_Coverage(i)

    def la_cov(self, operation, do_sampling=True):
        self.bits_cov[operation[0]].la_cov(operation, do_sampling)


class LA_Bit_Coverage():
    def __init__(self, bit) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.bit = bit
        self.la_cov(None, do_sampling=False)

    def la_cov(self, operation, do_sampling=True):
        @CoverPoint(
            f"top.caravel.user.logic_analyser.bit{self.bit}.in",
            xf=lambda operation: operation,
            bins=[(1, "in"), (0, "in")],
            bins_labels=["0 to 1", "1 to 0"],
            rel=lambda val, b: val[1] == b[0] and val[2] == b[1]
        )
        @CoverPoint(
            f"top.caravel.user.logic_analyser.bit{self.bit}.out",
            xf=lambda operation: operation,
            bins=[(1, "out"), (0, "out")],
            bins_labels=["0 to 1", "1 to 0"],
            rel=lambda val, b: val[1] == b[0] and val[2] == b[1]
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)
