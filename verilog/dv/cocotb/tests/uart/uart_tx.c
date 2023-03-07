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

#include <common.h>



// --------------------------------------------------------

void main(){
    enable_debug();
    enable_hk_spi(0);
    configure_gpio(6,GPIO_MODE_MGMT_STD_OUTPUT);

    // Set clock to 64 kbaud and enable the UART.  It is important to do this
    // before applying the configuration, or else the Tx line initializes as
    // zero, which indicates the start of a byte to the receiver.


    // Now, apply the configuration
    gpio_config_load();

//    reg_uart_clkdiv = 625;
    enable_uart_TX(1);

    set_debug_reg1(0xAA);

    // This should appear at the output, received by the testbench UART.
    // (Makes simulation time long.)
//    print("test msg\n");
    print("Monitor: Test UART (RTL) passed\n");

    // Allow transmission to complete before signalling that the program
    // has ended.
    dummy_delay(160);
}
