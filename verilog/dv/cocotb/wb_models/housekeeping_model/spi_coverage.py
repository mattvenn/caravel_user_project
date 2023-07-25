import cocotb
from cocotb_coverage.coverage import CoverPoint, CoverCross

class SPI_Coverage():
    def __init__(self) -> None:
        self.command_mapping = {
            "00000000": "no operation",
            "10000000": "write stream",
            "01000000": "read stream",
            "11000000": "write read stream",
            "11000100": "Pass-through management",
            "11000110": "Pass-through user",
        }
        self.command_mapping.update({f"10{format(n, '03b')}000": f"write {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"01{format(n, '03b')}000": f"read {n}-bytes" for n in range(1,8)})
        self.command_mapping.update({f"11{format(n, '03b')}000": f"write read {n}-bytes" for n in range(1,8)})
    
    def command_to_text(self, command):
        cocotb.log.debug(f"[{__class__.__name__}][command_to_text] command = {command}")
        if command in self.command_mapping:
            return self.command_mapping[command]
        else:
            return "invalid command"
        
    def spi_cov(self, spi_operation):
        @CoverPoint(
            "top.caravel.housekeeping.spi.modes",
            xf=lambda spi_operation: spi_operation.command,
            bins=[x for x in self.command_mapping.values()],
            weight=0
        )
        @CoverPoint(
            "top.caravel.housekeeping.spi.address",
            xf=lambda spi_operation: int(spi_operation.address, 16),
            bins=[(0, 0x10), (0x11, 0x20), (0x21, 0x30), (0x31, 0x40), (0x41, 0x50), (0x51, 0x60), (0x61, 0x6D)],
            bins_labels=["0 to 16", "17 to 32", "33 to 48", "49 to 64", "65 to 80", "81 to 96", "97 to 109"],
            rel=lambda val, b: b[0] <= val <= b[1],
            weight=0
        )
        def sample_command(spi_operation):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_write",
            xf=lambda data: int(data, 16),
            bins=[(0, 0), (1, 0xF), (0x10, 0xFF), (0xFF, 0xFF)],
            bins_labels=["zero", "1 to 15", "16 to 255", "255"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_write(data):
            pass

        @CoverPoint(
            "top.caravel.housekeeping.spi.data_read",
            xf=lambda data: int(data, 16),
            bins=[(0, 0), (1, 0xF), (0x10, 0xFF), (0xFF, 0xFF)],
            bins_labels=["zero", "1 to 15", "16 to 255", "255"],
            rel=lambda val, b: b[0] <= val <= b[1],
        )
        def sample_read(data):
            pass

        sample_command(spi_operation)
        for data in spi_operation.data_in:
            sample_write(data)
        for data in spi_operation.data_out:
            sample_read(data)

        @CoverCross(
            "top.caravel.housekeeping.spi.operations",
            items=[
                "top.caravel.housekeeping.spi.modes",
                "top.caravel.housekeeping.spi.address",
            ],
        )
        def sample():
            pass
        sample()