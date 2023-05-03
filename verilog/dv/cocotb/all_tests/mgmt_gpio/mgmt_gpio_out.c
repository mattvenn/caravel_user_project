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
    mgmt_gpio_o_enable();
    set_debug_reg1(10);
	for (int i = 0; i < 10; i++) {
		/* Fast blink for simulation */
		mgmt_gpio_wr(1);
		mgmt_gpio_wr(0);
	}
    set_debug_reg1(20);
	for (int i = 0; i < 20; i++) {
		/* Fast blink for simulation */
		mgmt_gpio_wr(1);
		mgmt_gpio_wr(0);
	}
    set_debug_reg1(0);
    set_debug_reg1(0); // for more delay
    set_debug_reg1(0);

    set_debug_reg2(0xFF); //finish test


}

