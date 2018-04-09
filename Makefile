
install:
	echo "#### Installing screen #####"
	sudo apt-get install screen
	echo "#### Patching scapy-radio (see Z3sec) #####"
	sudo cp `pwd`/patch/dot15d4.py /usr/local/lib/python2.7/dist-packages/scapy/layers/dot15d4.py

run:
	echo "#### Starting PIDZ #####"
	sudo python main.py

clean:
	echo "removing database"
	rm db/database





