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
 *	Management SoC GPIO Pin Test
 *		Tests writing to the GPIO pin.
 */

void main()
{
    enable_debug();
    enableHkSpi(0);
    ManagmentGpio_ioEnable();

    // pull up
    ManagmentGpio_write(1);
    set_debug_reg1(0x1B);

    // pull down
    ManagmentGpio_write(0);
    set_debug_reg1(0x2B);

    // no pull
    #ifndef REG_GPIO_INVERTED 
    reg_gpio_oe = 0; 
    #else
    reg_gpio_oe = 1; 
    #endif
    set_debug_reg1(0x3B);



}

