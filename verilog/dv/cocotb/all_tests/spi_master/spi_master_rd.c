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


    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x04);        // Write 0x04 (start address low byte)

    unsigned int value = MSPI_read(); // 0x93
    set_debug_reg1(value);

    value = MSPI_read(); // 0x01
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x18);        // Write 0x18 (start address low byte)

    value = MSPI_read(); // 0x44
    set_debug_reg1(value);

    value = MSPI_read(); // 0x33
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x22);        // Write 0x22 (start address low byte)

    value = MSPI_read(); // 0xC3
    set_debug_reg1(value);

    value = MSPI_read(); // 0xD0
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x37);        // Write 0x37 (start address low byte)

    value = MSPI_read(); // 0x89
    set_debug_reg1(value);

    value = MSPI_read(); // 0xa3
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x41);        // Write 0x41 (start address low byte)

    value = MSPI_read(); // 0x6B
    set_debug_reg1(value);

    value = MSPI_read(); // 0x8a
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x5f);        // Write 0x5f (start address low byte)

    value = MSPI_read(); // 0x77
    set_debug_reg1(value);

    value = MSPI_read(); // 0x5B
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x64);        // Write 0x64 (start address low byte)

    value = MSPI_read(); // 0xC7
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x70);        // Write 0x70 (start address low byte)

    value = MSPI_read(); // 0xB3
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x8c);        // Write 0x8c (start address low byte)

    value = MSPI_read(); // 0x48
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS
    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0x94);        // Write 0x94 (start address low byte)

    value = MSPI_read(); // 0xE7
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xaa);        // Write 0xaa (start address low byte)

    value = MSPI_read(); // 0x6F
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xb3);        // Write 0xb3 (start address low byte)

    value = MSPI_read(); // 0x30
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xc7);        // Write 0xc7 (start address low byte)

    value = MSPI_read(); // 0x2F
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xd8);        // Write 0xd8 (start address low byte)

    value = MSPI_read(); // 0x1C
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xeb);        // Write 0xeb (start address low byte)

    value = MSPI_read(); // 0xA0
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS

    MSPI_write(0x03);        // Write 0x03 (read mode)
    MSPI_write(0x00);        // Write 0x00 (start address high byte)
    MSPI_write(0x00);        // Write 0x00 (start address middle byte)
    MSPI_write(0xff);        // Write 0xff (start address low byte)

    value = MSPI_read(); // 0xFF
    set_debug_reg1(value);

    MSPI_enableCS(0);  // release CS
    MSPI_enableCS(1);  // sel=0, manual CS


    dummyDelay(100000000);
}

