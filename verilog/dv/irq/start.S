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
/* 000a :	Step count (0 to 5)		 */	
/* 000c-000f :	Last valid data position	 */
/* 0010-0028 :  Register store during IRQ	 */
/* 0030-0050 :	Test ring buffer		 */
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

	// Register use:
	// t0 :  SPI base address
	// t1 :  Step value
	// t2 :  Ring buffer position
	// t4 :  SPI read value
	// t5 :  Temporary values

	// Reset timer for a long count.  0x04000000 should correspond to
	// about 1 second at a 64MHz clock.  There are three steps to the
	// interrupt, so the timer should expire at 1/3 of the cycle time

	li   t5, 0x00002000
	picorv32_timer_insn(t5, t5)

	// This method works in three steps.  The step count is kept at address 10
	lb   t1, 10(zero)

	/* Increment the step count */
	addi t1, t1, 1

	/* If the step count is 3, set back to zero */
	addi t5, t1, -3
	bnez t5, irq_2
	sb   zero, 10(zero)
	j    irq_3

irq_2:
	/* Write back updated step count */
	sb   t1, 10(zero)

irq_3:
	/* Get ring buffer position 1 ahead (+2 bytes), and store in t2 */
	lw   t2, 12(zero)
	addi t2, t2, 2

	/* Wrap ring buffer at end (back to 0x30) */
	li   t5, 0x1000		// ends at memory address 0x1000
        blt  t2, t5, irq_4
	li   t5, 0x0fd0
	sub  t2, t2, t5
irq_4:

	/* Set SPI base address */
	/* (0x24000000 = config, 0x24000004 = data) */
	li   t0, 0x24000000

	/* Check if the step count is 3 */
	addi t5, t1, -3
	bnez t5, irq_6

	/* Read SPI byte */
	lb   t4, 4(t0)

	/* Store in next ring buffer position lower 8 bits */
	sb   t4, 0(t2)

	/* Update ring buffer address */
	sw   t2, 12(zero)

	/* Clear stream mode (clears CSB) */
	li	t5, 0x2082
	sh	t5, 0(t0)

	j irq_done
	
irq_6:
	/* Check if the step count is 2 */
	addi t5, t1, -2
	bnez t5, irq_7

	/* Step 2 only: */
	/* Read SPI byte */
	lb   t4, 4(t0)

	/* Store in next ring buffer position upper 8 bits */
	sb   t4, 1(t2)

irq_7:
	// Steps 1 and 2:

	/* Configure SPI for stream mode (sets CSB until cleared) */
	li	t5, 0x3082
	sh	t5, 0(t0)

	/* Initiate SPI transfer.  Write zero to reg_spi_data */
	sw	zero, 4(t0)

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

# Write these instructions to memory location zero and following:
# lui t4, 0x10000	= 10000eb7
# addi t4, t4, 4	= 0e91
# jalr t4, 0		= 000e80e7
#
# These three instructions jump to 0x10000004, which is the location
# of the interrupt handler.  For a fast interrupt handler, the whole
# handler should be moved into SRAM.

li  t4, 0x10000eb7
sw  t4, 0(zero)
li  t4, 0x80e70e91
sw  t4, 4(zero)
li  t4, 0x000e
sw  t4, 8(zero)

# Set step value (0) in memory position 0x000a
li   t0, 0x0000000a
sb   zero, 0(t0)

# Set ring buffer address (0x30) in memory position 0x000c
li   t4, 0x0030
sw   t4, 12(zero)

# Enable the timer IRQ only
li   t4, 0xfff0
picorv32_maskirq_insn(t4, t4)

# Set the picorv32 32-bit counter/timer to trigger the first interrupt.
# After that it's the responsibility of the irq() routine to deal with it.
# (see above)  The first interrupt is not timed and is longer than the
# 1/16MHz timing.

li t4, 0x2000
picorv32_timer_insn(t4, t4)

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

