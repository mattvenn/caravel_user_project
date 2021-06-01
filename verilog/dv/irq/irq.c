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

#include "verilog/dv/caravel/defs.h"
#include "verilog/dv/caravel/stub.c"

// -------------------------------------------------------------------------
// Test SPI interface running on a timed loop 
// -------------------------------------------------------------------------

// Ring buffer latest valid position held here
#define reg_ringbuf_ptr   (*(volatile uint32_t*)0x0000000c)
#define reg_ringbuf_start (*(volatile uint16_t*)0x00000030)

void main()
{
    uint16_t data;
    int i;

    // Configure GPIO upper bits to assert the test code
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_OUTPUT;

    // Configure GPIO lower bits to assert the data (16 bits)
    reg_mprj_io_31 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_30 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_29 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_OUTPUT;

    // Configure SPI pins (note:  opposite of housekeeping, which is default)
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    /* Apply the GPIO configuration */
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);

    /* Switch input disable = 0 to prevent SoC from driving SPI signals */
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_BIDIRECTIONAL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_BIDIRECTIONAL;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_BIDIRECTIONAL;

    reg_mprj_datah = 0x5;	// Signal start of test
    reg_mprj_datal = 0;

    // Note: SPI is enabled in the start.S routine, not needed here.

    // Loop, writing last received value from SPI to the GPIO

    while (1) {
        data = *((uint16_t *)(reg_ringbuf_ptr - 1)); 

	// Assert the most recent data capture on the GPIO lines
        reg_mprj_datal = (uint32_t)data << 16;

	// The following code shows the ring buffer address incrementing
        // reg_mprj_datal = (uint32_t)((int16_t *)(reg_ringbuf_ptr) << 16);

	if (data == 0x0a) break;
    }
    reg_mprj_datah = 0xa;	// Signal end of test
}

