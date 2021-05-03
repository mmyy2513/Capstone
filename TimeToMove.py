import socket

# socket init
host = '192.168.1.3'
port = 9997
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen()
conn, addr = s.accept()

# file name
fileName = "count_10min.txt"

while True:
	# Open file with read mode
	with open(fileName, "r") as f:
		
		# read last line ( num * 10 minutes = how long the patient doesn't move)
		last = f.readlines()[-1]

		# if last == 10 : he didnt move for 100 minutes
		if last == "10":
			print("MOVE!")

			# Send message to Rpi
			conn.send("MOVE".encode())
			while True:
				if conn.recv:
					break

			# Reset number of txt file, because we notice him
			with open(fileName, "w") as fw: pass
s.close()
				
	

