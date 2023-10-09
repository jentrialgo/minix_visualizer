"""This program analyzes a minix log file obtained using the Hacking the Minix Kernel
project, which can be found at https://oa.upm.es/68152/"""

import sys
import io


EVENTS = {
    0: {"event": "opIRQ_00", "parameters": 0, "name": "CLOCK_IRQ"},
    1: {"event": "opIRQ_01", "parameters": 0, "name": "KEYBOARD_IRQ"},
    2: {"event": "opIRQ_02", "parameters": 0, "name": "CASCADE_IRQ"},
    3: {"event": "opIRQ_03", "parameters": 0, "name": "ETHER_IRQ"},
    4: {"event": "opIRQ_04", "parameters": 0, "name": "RS232_IRQ"},
    5: {"event": "opIRQ_05", "parameters": 0, "name": "XT_WINI_IRQ"},
    6: {"event": "opIRQ_06", "parameters": 0, "name": "FLOPPY_IRQ"},
    7: {"event": "opIRQ_07", "parameters": 0, "name": "PRINTER_IRQ"},
    8: {"event": "opIRQ_08", "parameters": 0},
    9: {"event": "opIRQ_09", "parameters": 0},
    10: {"event": "opIRQ_10", "parameters": 0},
    11: {"event": "opIRQ_11", "parameters": 0},
    12: {"event": "opIRQ_12", "parameters": 0, "name": "KBD_AUX_IRQ"},
    13: {"event": "opIRQ_13", "parameters": 0},
    14: {"event": "opIRQ_14", "parameters": 0, "name": "AT_WINI_0_IRQ"},
    15: {"event": "opIRQ_15", "parameters": 0, "name": "AT_WINI_1_IRQ"},
    16: {"event": "opEXC_00", "parameters": 1, "name": "DIVIDE_VECTOR"},
    17: {"event": "opEXC_01", "parameters": 1, "name": "DEBUG_VECTOR"},
    18: {"event": "opEXC_02", "parameters": 1, "name": "NMI_VECTOR"},
    19: {"event": "opEXC_03", "parameters": 1, "name": "BREAKPOINT_VECTOR"},
    20: {"event": "opEXC_04", "parameters": 1, "name": "OVERFLOW_VECTOR"},
    21: {"event": "opEXC_05", "parameters": 1, "name": "BOUND_VECTOR"},
    22: {"event": "opEXC_06", "parameters": 1, "name": "INVALID_OPCODE_VECTOR"},
    23: {"event": "opEXC_07", "parameters": 1, "name": "COPROC_NOT_VECTOR"},
    24: {"event": "opEXC_08", "parameters": 1, "name": "DOUBLE_FAULT_VECTOR"},
    25: {"event": "opEXC_09", "parameters": 1, "name": "COPROC_SEG_VECTOR"},
    26: {"event": "opEXC_10", "parameters": 1, "name": "INVALID_TSS_VECTOR"},
    27: {"event": "opEXC_11", "parameters": 1, "name": "SEG_NOT_VECTOR"},
    28: {"event": "opEXC_12", "parameters": 1, "name": "STACK_FAULT_VECTOR"},
    29: {"event": "opEXC_13", "parameters": 1, "name": "PROTECTION_VECTOR"},
    30: {"event": "opEXC_14", "parameters": 1, "name": "PAGE_FAULT_VECTOR"},
    31: {"event": "opEXC_15", "parameters": 1, "name": "COPROC_ERR_VECTOR"},
    32: {"event": "opEXC_16", "parameters": 1, "name": "ALIGNMENT_VECTOR"},
    33: {"event": "opSVC_00", "parameters": 0},
    34: {"event": "opSVC_01", "parameters": 0, "name": "SEND"},
    35: {"event": "opSVC_02", "parameters": 0, "name": "RECEIVE"},
    36: {"event": "opSVC_03", "parameters": 0, "name": "SENDREC"},
    37: {"event": "opSVC_04", "parameters": 0, "name": "NOTIFY"},
    38: {"event": "opSVC_05", "parameters": 0, "name": "IPC_REQUEST"},
    39: {"event": "opSVC_06", "parameters": 0, "name": "IPC_REPLY"},
    40: {"event": "opSVC_07", "parameters": 0, "name": "IPC_NOTIFY"},
    41: {"event": "opSVC_08", "parameters": 0, "name": "ECHO"},
    42: {"event": "opSVC_09", "parameters": 0, "name": "IPC_RECEIVE"},
    43: {"event": "opMAPKBD", "parameters": 4},
    44: {"event": "opIDE", "parameters": 4 * 4},
}


def print_usage():
    print("Usage: python minix_visualizer.py <filename> [-v|-vv]")
    print("  -v: verbose")
    print("  -vv: very verbose")
    print("\nExample: python minix_visualizer.py log_e9.log -v")
    print(
        "\nThis program analyzes a minix log file, showing a summary of the keys pressed. "
        "If the-v option is used, it also shows every MAKEKBD event. "
        "If the -vv option is used, it shows every event."
    )
    sys.exit()


def analyze_log_file(log_file: io.IOBase, verbose_level: int) -> None:
    tick = 0
    keys_pressed = ""
    while True:
        byte = log_file.read(1)
        if not byte:
            break
        event = EVENTS.get(ord(byte))
        if event:
            if event["event"] == "opIRQ_00":
                if verbose_level == 2:
                    print(
                        f"\n*****************************| tick {tick} |*****************************\n"
                    )
                tick += 1

            if verbose_level == 2:
                if "name" in event:
                    print(event["event"], event["name"])
                else:
                    print(event["event"])

            if event["event"] == "opMAPKBD":
                parameters = log_file.read(event["parameters"])
                scan = parameters[0]
                asc_code = parameters[1]
                asc_ch = chr(asc_code) if asc_code > 30 else "-"

                # For the enter key (0x1c), there is a 2 byte code corresponding to the
                # clock counter, i.e., how many ticks are left until the next clock
                # interrupt.
                if scan == 28:
                    asc_ch = "ENTER"
                    cc = parameters[2] << 8 | parameters[3]
                    cc_msg = f" cc: {cc} "
                else:
                    cc = "-"
                    cc_msg = ""

                # Detect if it is a key press or release by checking the 7th bit
                is_press = scan & 0x80 == 0
                is_press_str = "press" if is_press else "release"

                if is_press and asc_ch != "-":
                    if asc_ch == "ENTER":
                        keys_pressed += "\n"
                    else:
                        keys_pressed += asc_ch

                if verbose_level > 0:
                    print(
                        f" scan code: {scan:2x} ascii: {asc_code:3} char: {asc_ch}{cc_msg} [{is_press_str}]"
                    )
            else:
                log_file.read(event["parameters"])  # skip parameters

    print("\n--- Keys pressed: ---\n")
    print(keys_pressed)


def main():
    if len(sys.argv) < 2:
        print_usage()

    filename = sys.argv[1]

    verbose_level = 0
    if len(sys.argv) > 2:
        if sys.argv[2] == "-v":
            verbose_level = 1
        elif sys.argv[2] == "-vv":
            verbose_level = 2
        else:
            print_usage()

    with open(filename, "rb") as log_file:
        analyze_log_file(log_file, verbose_level)


if __name__ == "__main__":
    main()
