import gopigo as go
import time

go.set_speed(130)

go.fwd()
go.led_on(0)
go.led_on(1)
time.sleep(1.9)
go.led_off(0)
go.led_off(1)
go.right()
go.led_on(0)
time.sleep(0.2)
go.fwd()
go.led_on(0)
go.led_on(1)
time.sleep(0.8)
go.led_off(0)
go.led_off(1)
go.left()
go.led_on(1)
time.sleep(0.8)

for i in range(4):
    go.right()
    go.led_on(0)
    time.sleep(0.1)
    go.fwd()
    go.led_on(0)
    go.led_on(1)
    time.sleep(0.2)
    go.led_off(0)
    go.led_off(1)


go.stop()
