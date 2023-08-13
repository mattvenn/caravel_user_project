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
    enable_debug();

    set_debug_reg2(0xAA); //wait for timer to send irq

    IRQ_clearFlag();
    /* Configure timer for a single-shot countdown */
    IRQ_enableTimer(1);
    timer0_configureOneShot(500);
    // Loop, waiting for the interrupt to change reg_mprj_datah
    char is_pass = 0;
    int timeout = 50; 
    unsigned int x;
    for (x = 0; x < timeout; x++){
        if (IRQ_getFlag() == 1){
            set_debug_reg1(0x1B); //test pass irq sent at timer0
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x1E); // timeout
    }
    IRQ_enableTimer(0);
    IRQ_enableTimer(1);
    // test interrupt doesn't happened when timer isnt used
    set_debug_reg2(0xBB);
    timer0_enable(0); // disable counter
    IRQ_clearFlag();
    // Loop, waiting for the interrupt to change reg_mprj_datah
    is_pass = 0;

    for (int i = 0; i < timeout; i++){
        if (IRQ_getFlag() == 1){
            set_debug_reg1(0x2E); //test fail interrupt isn't suppose to happened
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x2B); // test pass
    }

    // test finish 
    set_debug_reg2(0xFF);

}

