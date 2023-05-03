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

/*
 *	Management SoC GPIO Pin Test
 *		Tests writing to the GPIO pin.
 */

void main()
{
    enable_debug();
    enable_hk_spi(0);
    // enable input
    mgmt_gpio_i_enable();
    if (mgmt_gpio_rd() == 1)
        set_debug_reg2(0x1B); 
    else 
        set_debug_reg2(0x1E); 
    // disable input
    mgmt_gpio_io_disable();
    if (mgmt_gpio_rd() == 0)
        set_debug_reg2(0x2B); 
    else 
        set_debug_reg2(0x2E); 
    set_debug_reg2(0xFF);

    // enable output
    mgmt_gpio_o_enable();
    mgmt_gpio_wr(1);
    set_debug_reg1(0x1A);

    // disable output
    mgmt_gpio_i_enable();
    mgmt_gpio_wr(1);
    set_debug_reg1(0x2A);
}

