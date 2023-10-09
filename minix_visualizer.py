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

with open("log_e9.bin", "rb") as f:
    tick = 0
    keys_pressed = ""
    while True:
        byte = f.read(1)
        if not byte:
            break
        event = EVENTS.get(ord(byte))
        if event:
            if event["event"] == "opIRQ_00":
                print("\n*****************************")
                tick += 1

            if "name" in event:
                print(tick, event["event"], event["name"])
            else:
                print(tick, event["event"])

            if event["event"] == "opMAPKBD":
                parameters = f.read(event["parameters"])
                scan = parameters[0]
                asc_code = parameters[1]
                asc_ch = chr(asc_code) if asc_code > 30 else "-"

                # For the enter key (0x1c), there is a 2 byte code corresponding to the
                # clock counter, i.e., how many ticks are left until the next clock
                # interrupt.
                if scan == 28:
                    asc_ch = "\n"
                    cc = parameters[2] << 8 | parameters[3]
                else:
                    cc = "-"

                # Detect if it is a key press or release by checking the 7th bit
                is_press = scan & 0x80 == 0
                is_press_str = "press" if is_press else "release"

                if is_press and asc_ch != "-":
                    keys_pressed += asc_ch

                print(
                    f" scan code: {scan:2x} ascii: {asc_code:3} char: {asc_ch} cc: {cc} [{is_press_str}]"
                )
            else:
                f.read(event["parameters"])  # skip parameters

    print("Keys pressed:")
    print(keys_pressed)