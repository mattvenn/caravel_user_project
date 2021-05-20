# Wishbone demo

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![UPRJ_CI](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/user_project_ci.yml) [![Caravel Build](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml/badge.svg)](https://github.com/efabless/caravel_project_example/actions/workflows/caravel_build.yml)

This demo shows wishbone access to the user project. I have added a basic wishbone peripheral:

    https://github.com/mattvenn/wishbone-buttons-leds/tree/caravel

This provides 8 leds and 3 buttons that can be written and read via wishbone.

The module is instantiated inside [user_project_wrapper](verilog/rtl/user_project_wrapper.v).

The [firmware](verilog/dv/wb_buttons_leds/wb_buttons_leds.c) listens for all 3 buttons to be pressed, the lights all the 8 LEDS.

The [testbench](verilog/dv/wb_buttons_leds/wb_buttons_leds_tb.v) provides the button presses and finished when the lights are on.

# Setup

If you want to try this, then note it's using the MPW2 tools. Follow the [install instructions here to setup the PDK](docs/source/index.rst) 
You will also need a RISCV toolchain in order to compile the firmware.
