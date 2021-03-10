import serial
import re
import time
import pdb

class CSerial:
	def __init__(self, port, baudrate, timeout) :
		self.port = port
		self.baudrate = baudrate
		self.timeout = timeout
		self.buffer = ''
		self.portOpen = 0
	
	def Open(self) :
		self.serial = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
		if self.serial.isOpen() :
			self.portOpen = 1
		return self.serial
	
	def Close(self) :
		if self.portOpen == 1 :
			if self.serial.isOpen() :
				self.serial.close()
				self.portOpen = 0

	def send_cmd(self, cmd, terl) :	
		timeOut = 10 #sec
		timeStr = time.clock()
		#print self.serial.read(100)
		#self.serial.flushInput()
		#self.serial.flushOutput()
		
		self.serial.write(cmd.encode())
		

		#self.buffer = ''
		# No terminal string just tx
		if terl is '':
			return self.buffer

		while True:
			read = self.serial.read(self.serial.inWaiting())
			timeEnd = time.clock()
			if (timeEnd - timeStr) > timeOut:
				cmdRe = re.sub(r"\n", "\\\\n", cmd)
				print 'Wait to timeout, cmd \"' + cmdRe  + '\" no terminal \"' + terl + '\"\n'
				break
			self.buffer = self.buffer + read
			if terl in self.buffer:
				break
			#time.sleep(0.1)
			#if not self.serial.inWaiting():
			#	break

		#okre=re.compile(r"OK\n")
		#if okre.findall(buffer):
		#	rc = 1
		#else:
		#	rc = 0
		return self.buffer

	def tx(self, cmd) :
		#self.serial.flushInput()
		self.serial.flushOutput()
		self.serial.write(cmd.encode())
	
	def rx(self, terl, timeOut) :
		if timeOut <= 0 :
			timeOut = 5 #sec
		timeStr = time.time()
		rx_get = ''
		
		while True:	
			read = self.serial.read(self.serial.inWaiting())
			timeEnd = time.time()
			if (timeEnd - timeStr) > timeOut:
				print  'no terminal \"' + terl + '\"\n'
				break
			self.buffer = self.buffer + read
			if terl in self.buffer:
				#print '[rx]buffer = ' + self.buffer
				strP1, strP2 = self.buffer.split(terl, 1)
				#print 'strP1 = ' + strP1
				#print 'strP2 = ' + strP2
				self.buffer = strP2
				rx_get = strP1 + terl
				break
			#time.sleep(0.1)
			
		return rx_get

	def rx_inWaiting(self) :
		return self.serial.read(self.serial.inWaiting())

	def rx_size(self, size) :
		return self.serial.read(size)

	def rx_left(self) :
		while self.serial.inWaiting() is not 0 :	
			read = self.serial.read(self.serial.inWaiting())
			self.buffer = self.buffer + read
		print '[rx_left]buffer = ' + self.buffer	


	def clear(self) :
		while self.serial.inWaiting() > 0 :
			#print self.serial.inWaiting()
			read = self.serial.read(self.serial.inWaiting())
			self.buffer = self.buffer + read
		#print '[rx_left]buffer' + self.buffer	
		self.serial.flushInput()
		self.serial.flushOutput()
		rx_clear = self.buffer
		self.buffer = ''
		return rx_clear

def receiving(ser):
	global last_received
    
	buffer = ''
	while True:
		buffer = buffer + ser.read(ser.inWaiting())
		if 'cmd>' in buffer:
			print buffer
			break
	
def main(argv=None):
    
	message = "No Msg Responce!"    
	
	ser1 = CSerial("/dev/ttyUSB0", 115200, 5.0)
	
	print ser1.Open()

	#rc, resp = ser1.send_cmd("\n")	
	#print rc
	#print ("")
	#print resp
	rc, resp = ser1.send_cmd("set\n")	
	print rc
	print resp
	ser1.Close()

	'''
    try:
		print("Start Telnet Tool...")
		print("")
 
        #pdb.set_trace()
	
		port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=5.0)
		print port
		print port.read(100)

		#port.write("\n")
		#print port.read(100)
		port.flushInput()
		port.flushOutput()
		port.write("set\n")
		#print port.read(100)
		receiving(port)

    except Exception as e:
		print "Exception: %s" % e
		#tn.msg(message)
		#print(message)
		#print("")

		#print("End Telnet Tool...")
		#tn.close()
	'''	 
if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
