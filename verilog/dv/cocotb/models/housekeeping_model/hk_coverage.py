import cocotb
from cocotb_coverage.coverage import CoverPoint, CoverCross
from collections import namedtuple


class SPI_Coverage():
    def __init__(self) -> None:
        self.command_mapping = {
            "10000000": "write stream",
            "01000000": "read stream",
            "11000000": "write read stream",
            "11000100": "Pass-through management",
            "00000010": "Pass-through user",
        }
        self.command_mapping.update({f"10{format(n, '03b')}000": f"write {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"01{format(n, '03b')}000": f"read {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"11{format(n, '03b')}000": f"write read {n}-bytes" for n in range(1,8)})
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        temp = namedtuple('temp', ['command', 'address', 'data_in', 'data_out'])
        self.spi_cov(None, do_sampling=False)

    def command_to_text(self, command):
        cocotb.log.debug(f"[{__class__.__name__}][command_to_text] command = {command}")
        if command in self.command_mapping:
            return self.command_mapping[command]
        else:
            return "invalid command"

    def spi_cov(self, spi_operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.housekeeping.spi.modes",
            xf=lambda spi_operation: spi_operation.command,
            bins=[x for x in self.command_mapping.values()],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.spi.address",
            xf=lambda spi_operation: int(spi_operation.address, 16),
            bins=[(0, 0x10), (0x11, 0x20), (0x21, 0x30), (0x31, 0x40), (0x41, 0x50), (0x51, 0x60), (0x61, 0x6D)],
            bins_labels=["0 to 16", "17 to 32", "33 to 48", "49 to 64", "65 to 80", "81 to 96", "97 to 109"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
        )
        def sample_command(spi_operation):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_write",
            xf=lambda data: int(data, 16),
            bins=[(0x00, 0x0F), (0x10, 0x1F), (0x20, 0x2F), (0x30, 0x3F), (0x40, 0x4F), (0x50, 0x5F), (0x60, 0x6F), (0x70, 0x7F), (0x80, 0x8F), (0x90, 0x9F), (0xA0, 0xAF), (0xB0, 0xBF), (0xC0, 0xCF), (0xD0, 0xDF), (0xE0, 0xEF), (0xF0, 0xFF)],   
            bins_labels=["0x0 to 0x0F", "0x10 to 0x1F", "0x20 to 0x2F", "0x30 to 0x3F", "0x40 to 0x4F", "0x50 to 0x5F", "0x60 to 0x6F", "0x70 to 0x7F", "0x80 to 0x8F", "0x90 to 0x9F", "0xA0 to 0xAF", "0xB0 to 0xBF", "0xC0 to 0xCF", "0xD0 to 0xDF", "0xE0 to 0xEF", "0xF0 to 0xFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_write(data):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_read",
            xf=lambda data: int(data, 16),
            bins=[(0x00, 0x3F), (0x40, 0x7F), (0x80, 0xFF)],
            bins_labels=["0x00 to 0x3F", "0x40 to 0x7F", "0x80 to 0xFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_read(data):
            pass
        if do_sampling:
            sample_command(spi_operation)
            for data in spi_operation.data_in:
                sample_write(data)
            for data in spi_operation.data_out:
                sample_read(data)


class WB_Coverage():
    def __init__(self) -> None:
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized

        self.wb_cov(None, do_sampling=False)

    def wb_cov(self, wb_operation, do_sampling=True):
        @CoverPoint(
            "top.caravel.housekeeping.wishbone.access_type",
            xf=lambda wb_operation: wb_operation.write,
            bins=[0, 1],
            bins_labels=["read", "write"],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.wishbone.address",
            xf=lambda wb_operation: wb_operation.address,
            bins=[(0x26100000, 0x26100028), (0x26000000, 0x260000b8), (0x26200000, 0x26200010)],
            bins_labels=["spi address", "gpio address", "system address"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=1
        )
        @CoverPoint(
            "top.caravel.housekeeping.wishbone.write_data",
            xf=lambda wb_operation: wb_operation.write_data,
            bins=[(0x00000000, 0x5FFFFFFF),  (0x60000000, 0xBFFFFFFF), (0xC0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x5FFFFFFF", "0x60000000 to 0xBFFFFFFF", "0xC0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        @CoverPoint(
            "top.caravel.housekeeping.wishbone.read_data",
            xf=lambda wb_operation: wb_operation.read_data,
            bins=[(0x00000000, 0x5FFFFFFF),  (0x60000000, 0xBFFFFFFF), (0xC0000000, 0xFFFFFFFF)],
            bins_labels=["0 to 0x5FFFFFFF", "0x60000000 to 0xBFFFFFFF", "0xC0000000 to 0xFFFFFFFF"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample(wb_operation):
            pass
        if do_sampling:
            sample(wb_operation)
