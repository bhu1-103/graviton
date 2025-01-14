#!/usr/bin/env python3
NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

# Press 'y'
write_report(NULL_CHAR*2 + chr(28) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'o'
write_report(NULL_CHAR*2 + chr(18) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'u'
write_report(NULL_CHAR*2 + chr(24) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 't'
write_report(NULL_CHAR*2 + chr(23) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'u'
write_report(NULL_CHAR*2 + chr(24) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'b'
write_report(NULL_CHAR*2 + chr(5) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'e'
write_report(NULL_CHAR*2 + chr(8) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press '.' (period)
write_report(NULL_CHAR*2 + chr(55) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'c'
write_report(NULL_CHAR*2 + chr(6) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'o'
write_report(NULL_CHAR*2 + chr(18) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press 'm'
write_report(NULL_CHAR*2 + chr(16) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

# Press ENTER key
write_report(NULL_CHAR*2 + chr(40) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)

