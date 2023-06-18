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

void main(){
    enable_debug();
    enableHkSpi(0);
    ManagmentGpio_inputEnable();
    int num_blinks = 0;
    set_debug_reg1(0XAA); // start of the test
	while (1) {
        ManagmentGpio_wait(0);
        ManagmentGpio_wait(1);
        num_blinks++;
        if (get_debug_reg1() == 0xFF)
            break;
	}
    ManagmentGpio_outputEnable();
	for (int i = 0; i < num_blinks; i++) {
		/* Fast blink for simulation */
        ManagmentGpio_write(1);
        dummyDelay(10);
        ManagmentGpio_write(0);
        dummyDelay(10);
	}
    set_debug_reg2(0XFF); //finish test
    dummyDelay(10000000);
}

