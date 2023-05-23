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


void main(){
    enable_debug();
    enable_hk_spi(0);
    configure_gpio(6,GPIO_MODE_MGMT_STD_OUTPUT);
    configure_gpio(5,GPIO_MODE_MGMT_STD_INPUT_NOPULL);

    // Now, apply the configuration
    gpio_config_load();
    enable_uart_TX(1);
    uart_RX_enable(1);

    set_debug_reg1(0xAA); // configuration finished
    char* msg = uart_get_line();
    print(msg);

}
