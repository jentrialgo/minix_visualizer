# Minix Visualizer

This is a simple command line visualizer of log files generated with the [Hacking the
Minix Kernel project](https://oa.upm.es/68152/).

## Usage

```bash
python minix_visualizer.py <filename> [-v|-vv]
```

Example: 

```bash
python minix_visualizer.py log_e9.log -v
```

By default, it shows a summary of the keys pressed. If the `-v` option is used, it also
shows every `MAKEKBD` event. If the `-vv` option is used, it shows every event.

## Output

Example of non-verbose output:

```text
--- Keys pressed: ---

###usuario
echo John Doe
exit
root
halt
```

Example of verbose (`-v`) output:

```text
scan code: 24 ascii:  35 char: # [press]
scan code: 24 ascii:  35 char: # [press]
scan code: 1d ascii:   0 char: - [press]
scan code: 2e ascii:   3 char: - [press]
scan code: ae ascii:   3 char: - [release]
scan code: 9d ascii:   0 char: - [release]
scan code: 24 ascii:  35 char: # [press]
scan code: 16 ascii: 117 char: u [press]
scan code: 96 ascii: 117 char: u [release]
scan code: 1f ascii: 115 char: s [press]
scan code: 9f ascii: 115 char: s [release]
scan code: 16 ascii: 117 char: u [press]
scan code: 96 ascii: 117 char: u [release]
scan code: 1e ascii:  97 char: a [press]
 ...

 --- Keys pressed: ---

###usuario
echo John Doe
exit
root
halt
```
 
Example of very verbose (`-vv`) output:

```text
 opSVC_02 RECEIVE

*****************************| tick 0 |*****************************

opIRQ_00 CLOCK_IRQ
opSVC_02 RECEIVE
opSVC_02 RECEIVE
opSVC_03 SENDREC
opSVC_02 RECEIVE
opSVC_03 SENDREC
opSVC_02 RECEIVE
...
opMAPKBD
 scan code: 24 ascii:  35 char: # [press]
opSVC_03 SENDREC
opSVC_02 RECEIVE
...

 --- Keys pressed: ---

###usuario
echo John Doe
exit
root
halt
```
 