import re

class TxRxCmd:
    """Tx/Rx module"""
    def __init__(self):
        pass

    def serial_clear(self, uart) :
        resp = uart.clear()
        if len(resp) is 0 :
            return 0
        print resp
        return resp

    def command (self, uart, tx, rx = '', timeOut = 1, golden = 0) :
        rc = 0
        resp = ''
        okre = None
        self.serial_clear(uart)
        if len(rx) is 0 :
            self.serial_tx(uart, tx)
            rc = 1
        else :
            rc, resp = self.serial_tx_rx( uart,tx, rx, timeOut)
        return (rc, resp)

    def serial_tx(self, uart, cmd) :
        cmd = cmd + '\n'
        resp = uart.tx(cmd)
        print resp
        a=1

    def serial_rx (self, uart, key, timeOut=4) :
        rc = 0
        resp = ''
        okre = None

        resp = uart.rx(key, timeOut)
        okre = re.compile(key)

        if okre.findall(resp):
            rc = 1
        else:
            rc = 0
        return rc, resp

    def serial_tx_rx (self, uart, cmd, key, timeOut=1) :
        self.serial_tx(uart,cmd)
        rc, resp = self.serial_rx (uart, key, timeOut)
        return rc, resp

if __name__ == "__main__":
    print "txRxCmd as single program"