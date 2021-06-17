# Caravel User Project

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml) [![Caravel Build](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml)

---

# Multi Project Index

This index was made with [multi project tools](https://github.com/mattvenn/multi_project_tools)

The OpenLANE config was generated with this command:

    ./multi_tool.py --create-openlane-config --copy-gds  --force-delete

![multi macro](pics/multi_macro.png)

## RGB Mixer

* Author: Matt Venn
* Github: [https://github.com/mattvenn/wrapped_rgb_mixer/tree/caravel-mpw-two-c](https://github.com/mattvenn/wrapped_rgb_mixer/tree/caravel-mpw-two-c)
* commit: 19a96ea
* Description: reads 3 encoders and generates PWM signals to drive an RGB LED

![RGB Mixer](pics/schematic.jpg)

## Frequency counter

* Author: Matt Venn
* Github: [https://github.com/mattvenn/wrapped_frequency_counter/tree/caravel-mpw-two-c](https://github.com/mattvenn/wrapped_frequency_counter/tree/caravel-mpw-two-c)
* commit: c4aefe6
* Description: Counts pulses on input and displays frequency on 2  seven segment displays

![Frequency counter](pics/frequency_counter.png)

## A5/1 Wishbone

* Author: Jamie Iles
* Github: [https://github.com/jamieiles/a5-1-wb-macro](https://github.com/jamieiles/a5-1-wb-macro)
* commit: 0528740
* Description: A5/1 cryto block connected via wishbone to PicoRV32

![A5/1 Wishbone](pics/a5macro.png)

## Fibonacci

* Author: Konrad Rzeszutek Wilk
* Github: [https://github.com/konradwilk/fibonacci](https://github.com/konradwilk/fibonacci)
* commit: 3dcdd1b
* Description: Fibonacci emitter connected to [37:8] and controlled via wishbone

![Fibonacci](pics/fibonacci.png)

## Quad PWM FET Drivers

* Author: Chris DePalm
* Github: [https://github.com/ChrisDePalm/wrapped_quad_pwm_fet_drivers.git](https://github.com/ChrisDePalm/wrapped_quad_pwm_fet_drivers.git)
* commit: 547d9e1
* Description: 4 PWM FET Drivers for Power Applications

![Quad PWM FET Drivers](pics/wrapped_quad_pwm_fet_drivers.gds.png)

## memLCDdriver

* Author: Matt Beach
* Github: [https://github.com/matt-beach/wrapped_memLCDdriver.git](https://github.com/matt-beach/wrapped_memLCDdriver.git)
* commit: 07e07f9
* Description: SPI to 64-color memory LCD interface

![memLCDdriver](pics/wrapped_memLCDdriver.gds.png)

## QARMA-64 Accelerator

* Author: Viktor H. Brange
* Github: [https://github.com/vbrange/verilog_qarma](https://github.com/vbrange/verilog_qarma)
* commit: 8a10211
* Description: Implementation of QARMA 64

![QARMA-64 Accelerator](pics/qarma.png)

## ChaCha20 Accelerator

* Author: Richard Petri
* Github: [https://github.com/rpls/wrapped_chacha_wb_accel](https://github.com/rpls/wrapped_chacha_wb_accel)
* commit: a312d9d
* Description: A minimal Wishbone connected ChaCha20 accelerator

![ChaCha20 Accelerator](pics/core.png)

## Framebufferless Video Core

* Author: Tom Gwozdz
* Github: [https://github.com/tomgwozdz/fbless-graphics-core](https://github.com/tomgwozdz/fbless-graphics-core)
* commit: fdd7f04
* Description: A framebufferless VGA video generator, under CPU control

![Framebufferless Video Core](pics/fbless_graphics_core.gds.png)

## Pong

* Author: Erik van Zijst
* Github: [https://github.com/erikvanzijst/wrapped_pong.git](https://github.com/erikvanzijst/wrapped_pong.git)
* commit: 8506f61
* Description: A hardware implementation of Pong

![Pong](pics/pong.jpg)

## Hack soc

* Author: Maximo Balestrini
* Github: [https://github.com/mbalestrini/wrapped_hack_soc](https://github.com/mbalestrini/wrapped_hack_soc)
* commit: 416d3ec
* Description: Hardware implementation of the Hack Computer from the Nand to Tetris courses

![Hack soc](pics/project.jpg)

## gfxdemo

* Author: Konrad Beckmann
* Github: [https://github.com/kbeckmann/wrapped_gfxdemo](https://github.com/kbeckmann/wrapped_gfxdemo)
* commit: 432874a
* Description: gfxdemo

![gfxdemo](pics/gfxdemo.png)

## Wishbone HyperRAM

* Author: Pawel Sitarz
* Github: [https://github.com/embelon/wrapped_wb_hyperram](https://github.com/embelon/wrapped_wb_hyperram)
* commit: 5e793ea
* Description: Simple HyperRAM driver accesible on Wishbone bus

![Wishbone HyperRAM](pics/HyperRAM_WriteMemorySpace.png)

## Newmot SoC

* Author: Charles-Henri Mousset
* Github: [https://github.com/chmousset/caravel_multi_newmot](https://github.com/chmousset/caravel_multi_newmot)
* commit: e34a612
* Description: Simple SoC dmonstrating a Stepper Motor step/dir generator, and litex wishbone / uart / pwm

![Newmot SoC](pics/newmot.png)

## hoggephase

* Author: David Hulton
* Github: [https://github.com/h1kari/wrapped_hoggephase_project](https://github.com/h1kari/wrapped_hoggephase_project)
* commit: 3dbdd48
* Description: Hogge Phase EMFI/BBI Glitch Detector

![hoggephase](pics/hpcore.png)

## bfloat16_fma

* Author: Author
* Github: [https://github.com/etalian/mensa](https://github.com/etalian/mensa)
* commit: 2b61fe3
* Description: dual bfloat16 fused multiply-add

![bfloat16_fma](pics/wrapped_bfloat16.gds.png)

