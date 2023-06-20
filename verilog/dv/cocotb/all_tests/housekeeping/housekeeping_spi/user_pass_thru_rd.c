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





void main()
{
    // This program is just to keep the processor busy while the
    // housekeeping SPI is being accessed. to show that the
    // processor is halted while the SPI is accessing the
    // flash SPI in pass-through mode.
   enable_debug();

    // Management needs to apply output on these pads to access the user area SPI flash
    GPIOs_configure(11 ,GPIO_MODE_MGMT_STD_INPUT_NOPULL); // SDI
    GPIOs_configure(10 ,GPIO_MODE_MGMT_STD_OUTPUT); // SDO
    GPIOs_configure(9  ,GPIO_MODE_MGMT_STD_OUTPUT); // clk
    GPIOs_configure(8  ,GPIO_MODE_MGMT_STD_OUTPUT); // csb
    GPIOs_configure(1  ,GPIO_MODE_MGMT_STD_OUTPUT); // SDI housekeeping spi

    GPIOs_loadConfigs();


    // Start test
    set_debug_reg1(0xAA);
    set_debug_reg1(0xBB);
    dummyDelay(100000000);
}

