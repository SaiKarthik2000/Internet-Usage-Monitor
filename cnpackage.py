# 19pd18 19pd28 CN Package
# Internet Usage Monitor
import speedtest
import psutil
import os
import time
import tkinter as tk
from tkinter import *

def downspeed():
	st = speedtest.Speedtest()
	sp=[]
	for i in range(3):
		sp.append(st.download()/(1024*1024))
	string = "The download speed is " + str(max(sp))
	label = Label(root1, text = string)
	label.pack()

def upspeed():
	st = speedtest.Speedtest()
	sp=[]
	for i in range(3):
		sp.append(st.upload()/(1024*1024))
	string = "The upload speed is " + str(max(sp))
	label = Label(root1, text = string)
	label.pack()

def speed():
	global root1 
	root1 = tk.Tk()
	root1.minsize(300,300)
	root1.title("Speed Test")
	frame = tk.Frame(root1)
	frame.pack()
	slogan = tk.Button(frame,text="Download",command=downspeed)
	slogan.pack(side=tk.LEFT, pady = 100)
	slogan = tk.Button(frame,text="Upload",command=upspeed)
	slogan.pack(side=tk.LEFT, pady = 100)
	slogan = tk.Button(frame,text="Close",command=root1.destroy)
	slogan.pack(side=tk.LEFT, pady = 100)
	root1.mainloop()
	
def usage():
	NETWORK_INTERFACE = 'enp0s3'
	NETWORK_LIMIT = 5242880
	flag1,flag2,flag3=0,0,0
	netio = psutil.net_io_counters(pernic=True)
	t0=time.time()
	old_up = netio[NETWORK_INTERFACE].bytes_sent
	old_down = netio[NETWORK_INTERFACE].bytes_recv
	old_net_usage = old_up + old_down
	while True:
		netio = psutil.net_io_counters(pernic=True)
		up = netio[NETWORK_INTERFACE].bytes_sent
		down = netio[NETWORK_INTERFACE].bytes_recv
		t1=time.time()
		upspeed = (up-old_up)/(t1-t0)/1024.0
		downspeed = (down-old_down)/(t1-t0)/1024.0
		t0=t1
		old_up=up
		old_down=down
		net_usage = old_up + old_down
		print((net_usage-old_net_usage)/1024," kb is used")
		print("Current upload speed is ",upspeed," kbps")
		print("Current download speed is ",downspeed," kbps")
		if (net_usage-old_net_usage) > (NETWORK_LIMIT)*0.5 and flag1==0:
			print("50% of network limit reached")
			flag1=1
		if (net_usage-old_net_usage) > (NETWORK_LIMIT)*0.9 and flag2==0:
			print("90% of network limit reached")
			flag2=1
		if (net_usage-old_net_usage) > NETWORK_LIMIT and flag3==0:
			print("Meets network limit!")
			flag3=1
			disable_wifi = "nmcli con down 'Wired connection 1'"
			os.popen(disable_wifi)
			break
		if KeyboardInterrupt:
			print("")
		time.sleep(5)

def bandwidth():
	old_value = 0
	while True:
		new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
		if old_value:
			send_stat(new_value - old_value)
		old_value = new_value
		if KeyboardInterrupt:
			print("")
		time.sleep(1)

def convert_to_mbit(value):
    	return value/1024./1024.*8

def send_stat(value):
    	print("%0.3f" % convert_to_mbit(value))
    	
if __name__=='__main__':
	root = tk.Tk()
	root.minsize(350,350)
	root.title("Internet Usage Monitor")
	frame = tk.Frame(root)
	frame.pack()
	slogan = tk.Button(frame,text="Speed Test",command=speed)
	slogan.pack(side=tk.LEFT, pady = 100)
	slogan = tk.Button(frame,text="Usage",command=usage)
	slogan.pack(side=tk.LEFT, pady = 100)
	slogan = tk.Button(frame,text="band",command=bandwidth)
	slogan.pack(side=tk.LEFT, pady = 100)
	root.mainloop()
	