class ROI:
    def __init__(self, x=0, y=0, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def apply(self, frame):
        if self.w is None or self.h is None:
            return frame  # ROI desativada
        return frame[self.y:self.y+self.h, self.x:self.x+self.w]