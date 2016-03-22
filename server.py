import socket

s=socket.socket()

# Get local machine name
host=socket.gethostname()
port= #Open Port <int>
s.bind((host, port))

s.listen(5)
while True:
	c,addr=s.accept() 			# Establish connection with client
	print 'Got conxn from', addr
	c.send('Thank you for connecting')
	c.close()					# Close the connection


