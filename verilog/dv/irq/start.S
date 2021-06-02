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

/*-----------------------------------------------*/
/* Start code that enables and handles IRQs 	 */
/*-----------------------------------------------*/
/* Code modified specifically for this testbench */
/*-----------------------------------------------*/
/* Memory addresses reserved:			 */
/* 000a :	register for flagging the interrupt */	
/*-----------------------------------------------*/

#undef ENABLE_FASTIRQ

#include "custom_ops.S"

.section .text
.global irq

reset_vec:
	j start

/* Interrupt handler @ 0x10000004 */

.balign 4
irq_vec:
	/* save registers at address 0x10 to 0x24 */

        sw gp,   0*4+0x10(zero)
        sw x1,   1*4+0x10(zero)
        sw x3,   3*4+0x10(zero)
        sw x4,   4*4+0x10(zero)
        sw x5,   5*4+0x10(zero)

    # Set special reg to 0
    li   t0, 0x0000000a
    sb   zero, 0(t0)

	j irq_done
	

irq_done:
        /* restore registers */

        lw gp,   0*4+0x10(zero)
        lw x1,   1*4+0x10(zero)
        lw x2,   2*4+0x10(zero)
        // do not restore x3 (gp)
        lw x4,   4*4+0x10(zero)
        lw x5,   5*4+0x10(zero)

        picorv32_retirq_insn()

irq_regs:
        // registers are saved to this memory region during interrupt handling
        // the program counter is saved as register 0
        .fill 32,4

        // stack for the interrupt handler
        .fill 128,4
irq_stack:

/* Main program */

start:

# zero-initialize register file
addi x1, zero, 0
# x2 (sp) is initialized by reset
addi x3, zero, 0
addi x4, zero, 0
addi x5, zero, 0
addi x6, zero, 0
addi x7, zero, 0
addi x8, zero, 0
addi x9, zero, 0
addi x10, zero, 0
addi x11, zero, 0
addi x12, zero, 0
addi x13, zero, 0
addi x14, zero, 0
addi x15, zero, 0
addi x16, zero, 0
addi x17, zero, 0
addi x18, zero, 0
addi x19, zero, 0
addi x20, zero, 0
addi x21, zero, 0
addi x22, zero, 0
addi x23, zero, 0
addi x24, zero, 0
addi x25, zero, 0
addi x26, zero, 0
addi x27, zero, 0
addi x28, zero, 0
addi x29, zero, 0
addi x30, zero, 0
addi x31, zero, 0

# zero initialize scratchpad memory
# setmemloop:
# sw zero, 0(x1)
# addi x1, x1, 4
# blt x1, sp, setmemloop

# Enable the user interrupts only on irq[14:12]
# https://github.com/efabless/caravel-lite/blob/13f2590e4b3a74b910dac56a6b757f5a66fd5212/verilog/rtl/mgmt_soc.v#L360
li   t4, 0x7000 
picorv32_maskirq_insn(t4, t4)

# call main
call main
loop:
j loop

.global flashio_worker_begin
.global flashio_worker_end

flashio_worker_begin:
# a0 ... data pointer
# a1 ... data length
# a2 ... optional WREN cmd (0 = disable)

# address of SPI ctrl reg
li   t0, 0x02000000

# Set CS high, IO0 is output
li   t1, 0x120
sh   t1, 0(t0)

# Enable Manual SPI Ctrl
sb   zero, 3(t0)

# Send optional WREN cmd
beqz a2, flashio_worker_L1
li   t5, 8
andi t2, a2, 0xff
flashio_worker_L4:
srli t4, t2, 7
sb   t4, 0(t0)
ori  t4, t4, 0x10
sb   t4, 0(t0)
slli t2, t2, 1
andi t2, t2, 0xff
addi t5, t5, -1
bnez t5, flashio_worker_L4
sb   t1, 0(t0)

# SPI transfer
flashio_worker_L1:
beqz a1, flashio_worker_L3
li   t5, 8
lbu  t2, 0(a0)
flashio_worker_L2:
srli t4, t2, 7
sb   t4, 0(t0)
ori  t4, t4, 0x10
sb   t4, 0(t0)
lbu  t4, 0(t0)
andi t4, t4, 2
srli t4, t4, 1
slli t2, t2, 1
or   t2, t2, t4
andi t2, t2, 0xff
addi t5, t5, -1
bnez t5, flashio_worker_L2
sb   t2, 0(a0)
addi a0, a0, 1
addi a1, a1, -1
j    flashio_worker_L1
flashio_worker_L3:

# Back to MEMIO mode
li   t1, 0x80
sb   t1, 3(t0)

ret
flashio_worker_end:

