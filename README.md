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
* Description: reads 3 encoders and generates PWM signals to drive an RGB LED

![RGB Mixer](pics/schematic.jpg)

## Frequency counter

* Author: Matt Venn
* Github: [https://github.com/mattvenn/wrapped_frequency_counter/tree/caravel-mpw2](https://github.com/mattvenn/wrapped_frequency_counter/tree/caravel-mpw2)
* Description: Counts pulses on input and displays frequency on 2  seven segment displays

![Frequency counter](pics/frequency_counter.png)

## A5/1 Wishbone

* Author: Jamie Iles
* Github: [https://github.com/jamieiles/a5-1-wb-macro](https://github.com/jamieiles/a5-1-wb-macro)
* Description: A5/1 cryto block connected via wishbone to PicoRV32

![A5/1 Wishbone](pics/a5macro.png)

