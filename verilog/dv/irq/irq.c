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

volatile bool flag;

// gets jumped to from the interrupt handler defined in start.S
uint32_t *irq()
{
    flag = 0;
}

void main()
{
    flag = 1;

    // Configure GPIO upper bits to assert the test code
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_33 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_32 = GPIO_MODE_MGMT_STD_OUTPUT;

    /* Apply the GPIO configuration */
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);

    reg_mprj_irq = 0b001; // enable only user irq 0, which maps to picorv32 irq 12

    reg_mprj_datah = 0x5;	// Signal start of test
    reg_mprj_datal = 0;

    // setup interrupt generator
	reg_la0_oenb = reg_la0_iena = 0x0;    // enable output, disable inputs from user area
    reg_la0_data = 500 + (1 << 16); // set the count down value and trigger the start of the timer
    reg_la0_data = 0;

    // wait for interrupt to be raised, the interrupt routine defined in start.S will set it to 0
    while (flag) {
    }

    // Signal 2nd interrupt test
    reg_mprj_datah = 0x6;	
    // reset flag
    flag = 1;

    reg_la0_data = 500 + (1 << 16); // set the count down value and trigger the start of the timer
    reg_la0_data = 0;

    while (flag) {
    }

    // Signal end of test
    reg_mprj_datah = 0xa;	
}

