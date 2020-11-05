import gopigo as go
import time

for i in range(5):
    go.set_speed(191)
    go.fwd()
    time.sleep(1)
    go.bwd()
    time.sleep(1)
go.stop()
