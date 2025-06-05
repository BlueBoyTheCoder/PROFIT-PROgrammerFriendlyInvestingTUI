from enum import IntEnum

class TimeFrameInt(IntEnum):
    M15 = 15
    M30 = 30
    H1 = 60
    H2 = 120
    H4 = 240
    H8 = 480
    H16 = 960
    D2 = 1920
    D4 = 3840
    D8 = 7680
    D16 = 15360
    D32 = 30720
    D64 = 61440
