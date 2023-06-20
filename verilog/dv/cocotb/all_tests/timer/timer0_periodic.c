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



void main(){
    unsigned int value;
    unsigned int old_value;
    enable_debug();
    enableHkSpi(0);

    /* Configure timer for a periodic countdown */
	timer0_configurePeriodic(0x300);

    // Loop, waiting for the interrupt to change reg_mprj_datah
    // test path if counter value stop updated after reach 0 and also the value is always decrementing
    timer0_updateValue(); // update reg_timer0_value with new counter value
    old_value = timer0_readValue();
    // value us decrementing until it reachs zero and rollover to 0x300 (initial value)
    int rollover = 0;
    int timeout = 400; 
    for (int i = 0; i < timeout; i++){
        timer0_updateValue(); // update reg_timer0_value with new counter value
        value = timer0_readValue();
        if (value > old_value){
            rollover++;
            if (rollover==1)
                set_debug_reg1(0x1B); // timer rollover
            else if (rollover==2)
                set_debug_reg1(0x2B); //timer rollover second time
            else if (rollover==3){
                set_debug_reg1(0x3B); //timer rollover third time
                break;
            }
        }
        if (value < old_value){
            set_debug_reg1(0x4B); // value decreases
        }
	    old_value = value;
    }

    if (rollover ==0){
        set_debug_reg1(0xEE); //  counter didn't rollover
    }
    set_debug_reg2(0xFF); // finish test

}

