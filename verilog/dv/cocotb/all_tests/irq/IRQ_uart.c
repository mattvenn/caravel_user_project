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
    IRQ_clearFlag();
    GPIOs_configure(6,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_loadConfigs();
    IRQ_enableUartTx(1);

    set_debug_reg2(0xAA); //start sending data through the uart
    print("M");

    // Loop, waiting for the interrupt to change reg_mprj_datah
    char is_pass = 0;
    int timeout = 100; 

    for (int i = 0; i < timeout; i++){
        if (IRQ_getFlag() == 1){
            set_debug_reg1(0x1B); //test pass irq sent
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x1E); // timeout
    }
    // test interrupt doesn't happened nothing sent at uart
    set_debug_reg2(0xBB);
    IRQ_enableUartTx(0);
    IRQ_enableUartTx(1);
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

