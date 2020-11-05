import gopigo as go
import time

go.set_speed(130)

for i in range(4):
    go.fwd()
    time.sleep(0.5)
    go.right()
    time.sleep(0.5)

go.stop()