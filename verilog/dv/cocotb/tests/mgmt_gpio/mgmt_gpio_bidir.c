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

void main(){
    enable_debug();
    enable_hk_spi(0);
    mgmt_gpio_i_enable();
    int num_blinks = 0;
    set_debug_reg1(0XAA); // start of the test
	while (1) {
        wait_gpio_mgmt(0);
        wait_gpio_mgmt(1);
        num_blinks++;
        if (get_debug_reg1() == 0xFF)
            break;
	}
    mgmt_gpio_o_enable();
	for (int i = 0; i < num_blinks; i++) {
		/* Fast blink for simulation */
        mgmt_gpio_wr(1);
        dummy_delay(10);
        mgmt_gpio_wr(0);
        dummy_delay(10);
	}
    set_debug_reg2(0XFF); //finish test
    dummy_delay(10000000);
}

