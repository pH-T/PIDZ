
install:
	echo "installing screen"
	sudo apt-get install screen
	echo "patching scapy-radio"
	echo "see Z3sec"
	sudo cp `pwd`/patch/dot15d4.py /usr/local/lib/python2.7/dist-packages/scapy/layers/dot15d4.py

run:
	echo "creating new screen PIDZ"
	screen -dmS PIDZ bash -c 'sudo python main.py'

clean:
	echo "removing database"
	rm db/database





