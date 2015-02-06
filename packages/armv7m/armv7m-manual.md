<!---
     Copyright (c) 2015 National ICT Australia Limited (NICTA), ABN 62 102 206 173.
     All rights reserved.
  -->

%title ARMv7M package: user manual
%version 1-draft
%docid GQH8W1

Introduction
-------------

The ARMv7M package provides the following modules:

<dl>
  <dt>`build`</dt>
  <dd>A build module.</dd>

  <dt>`vectable`</dt>
  <dd>A module that generates an appropriate vector table, default linker script, and bitband.h header.</dd>
</dl>


`armv7m/build`
==============

The build module supports the *system build* interface.
The module does not support any options.
For correct operation, the system must include at least one C or assembler file.
The system must also have an assigned linker-script.
It is recommended that the vectable module is used to provide a functional linker-script.

`armv7m/vectable`
==============

The vectable module controls the generation of `vectable.s` and `default.ld`, as well as providing the `bitband.h` header file, which is used by the RTOS.

`vectable.s` implements:

* the system vector table (i.e.: interrupt dispatch table), which is at the fixed address 0x0.
* the low-level `entry` function, which is responsible for initializing `.data` and `.bss` before jumping to `main`.
* the default `reset` exception handler.

When using `prj` in configuration mode, the user may prefer to use a custom hand-written `vectable.s` rather than the one generated by the `armv7m.vectable` module.

`default.ld` generates a linker-script that is suitable for use with the GNU linker.
Although it is possible to use an alternative linker script, care must be taken to ensure it contains the necessary symbol declarations, and to ensure that sections are grouped in an appropriate manner.

The `bitband.h` header defines a number of special macros which are used to simplify the use of the ARM *bitband* feature.
The *bitband* feature allows atomic access to individual bits within words, and forms a critical piece of the RTOS implementation.
In addition to the macro expansion used by the compiler, uses of the macro are also parsed by the `armv7m.vectable` module and used to populate the `default.ld` file with the appropriate symbol aliases.

Note: When using `prj` in configuration only mode, the `bitband.h` header can not be used by code other than the RTOS itself.

The `armv7m.vectable` module supports a number of (optional) configuration options.

A subset of the individual exceptions (whose handlers occupy the entries 0..15 of the vector table) may be configured through the following configuration options:

* `nmi`
* `hardfault`
* `memmanage`
* `busfault`
* `usagefault`
* `svcall`
* `debug_monitor`
* `pendsv`
* `systick`

Each of these configurations has the type *C identifier*, and defaults to `reset`.

Additionally, individual IRQs (whose handlers occupy entries 16..255 of the vector table) can be configured via the `external_irq` configuration option, which consists of the child options:

* `number`, the IRQ number of the IRQ vector to be configured.
* `handler`, the C identifier of the IRQ's handler function.

Note that IRQ numbers 0..239 map to exception numbers 16..255, where the exception number corresponds to the IRQ vector's place in the vector table.
Individual IRQ vector table entries default to handler `reset` if not specified via an `external_irq` configuration.

The C identifier type are all ASCII strings which are valid identifiers in the C language.
In all cases, the identifier must refer to a function which the application implements and the RTOS invokes when the corresponding exception occurs.
Such functions must have the signature `void f(void)`.
No checks are performed during configuration to ensure the specified exception handler function is available.
Subsequent linker errors will occur if the exception handler is incorrectly specified.

The boolean option `preemption` must be set to `true` for systems on RTOS variants with preemption support.
The option defaults to `false` if not specified.
If preemption support is enabled, the `pendsv` and `svcall` vectors are not available for configuration.

The other options available for the `armv7m.vectable` module control the memory layout.
The correct values for these items generally require consultation with the chip reference manual.
The following values are configurable (defaults appear in parentheses):

* flash_load_addr (0x0)
* code_addr (0x0)
* data_addr (0x2000.0000)
* bitband_base (0x2000.0000)
* bitband_size (0x100.0000)
* bitband_alias (0x2200.0000)

Finally, there is an option (`stack_size`) for specifying the initial stack size in bytes.
This stack is used by the `main` function up until the RTOS is actually started.
The default stack size is 4096 bytes.