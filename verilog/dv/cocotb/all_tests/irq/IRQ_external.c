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


/*
Testing timer interrupts 
Enable interrupt for IRQ external pin mprj_io[7] -> should be drived to 1 by the environment
**NOTE** housekeeping SPI should used to update register irq_1_inputsrc to 1 see verilog code

    @wait for environment to make mprj[7] high
        send 0xAA

    @received interrupt correctly  test pass
        send 0x1B

    @ timeout                       test fail
        send 0x1E

    @ end test 
        send 0xFF
*/


void main(){
    enable_debug();
    // setting bit 7 as input 
    GPIOs_configure(7,GPIO_MODE_MGMT_STD_INPUT_NOPULL);

    GPIOs_loadConfigs();
    IRQ_enableExternal1(1);

    // test interrrupt happen when mprj[7] is asserted
    IRQ_clearFlag();
    set_debug_reg2(0xAA); //wait for environment to make mprj[7] high 
    // Loop, waiting for the interrupt to change reg_mprj_datah
    char is_pass = 0;
    int timeout = 40; 

    for (int i = 0; i < timeout; i++){
        if (IRQ_getFlag() == 1){
            set_debug_reg1(0x1B); //test pass irq sent at mprj 7 
            is_pass = 1;
            break;
        }
    }
    if (!is_pass){
        set_debug_reg1(0x1E); // timeout
    }

    // test interrupt doesn't happened when mprj[7] is deasserted
    set_debug_reg2(0xBB);
    IRQ_enableExternal1(0);
    IRQ_enableExternal1(1);
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
