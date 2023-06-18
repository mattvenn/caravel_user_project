/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */


#include <firmware_apis.h>



// --------------------------------------------------------

/*
 *	SPI master Test
 *	- Enables SPI master
 *	- Uses SPI master to talk to external SPI module
 */


void main(){
    enable_debug();
    enableHkSpi(0);

    GPIOs_configure(34,GPIO_MODE_MGMT_STD_INPUT_NOPULL); // SDI
    GPIOs_configure(35,GPIO_MODE_MGMT_STD_OUTPUT);       // SDO
    GPIOs_configure(33,GPIO_MODE_MGMT_STD_OUTPUT);       // CSB
    GPIOs_configure(32,GPIO_MODE_MGMT_STD_OUTPUT);       // SCK

    // Now, apply the configuration
    GPIOs_loadConfigs();
    set_debug_reg2(0xAA);
    MSPI_enable(1);


    // For SPI operation, GPIO 1 should be an input, and GPIOs 2 to 4
    // should be outputs.

    // Start test

    // Enable SPI master
    // SPI master configuration bits:
    // bits 7-0:	Clock prescaler value (default 2)
    // bit  8:		MSB/LSB first (0 = MSB first, 1 = LSB first)
    // bit  9:		CSB sense (0 = inverted, 1 = noninverted)
    // bit 10:		SCK sense (0 = noninverted, 1 = inverted)
    // bit 11:		mode (0 = read/write opposite edges, 1 = same edges)
    // bit 12:		stream (1 = CSB ends transmission)
    // bit 13:		enable (1 = enabled)
    // bit 14:		IRQ enable (1 = enabled)
    // bit 15:		(unused)

    // reg_spimaster_clk_divider = 0x4E20;
    MSPI_enableCS(1);  // sel=0, manual CS
    MSPI_write(0x08);        // Write 0x03 (read mode)
    MSPI_write(0x05);        // Write 0x00 (start address high byte)
    unsigned int value = MSPI_read(); // 0x93
    if (value == 0xD)
        set_debug_reg1(0xBB); // get correct value
    else {
        set_debug_reg2(value);
        set_debug_reg1(0xEE); // get wrong value
    }

    MSPI_enableCS(0);  // release CS
    // reg_spimaster_clk_divider = 0x4E00;

    MSPI_enableCS(1);  // sel=0, manual CS
    MSPI_write(0x08);        // Write 0x03 (read mode)
    MSPI_write(0x05);        // Write 0x00 (start address high byte)

    dummyDelay(100000000);
}

