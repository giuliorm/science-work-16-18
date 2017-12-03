class TimeUnits:
    def __init__(self):
        self.time_units = {}

class TimeUnit:
    def __init__(self, name, time, tx, ty, tz, rx, ry, rz, sx,sy,sz):
        self.name = name
        self.time = time
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.sx = sx
        self.sy = sy
        self.sz = sz