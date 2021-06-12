help:
	@egrep '^\w+:' Makefile

# must sudo because we are using bcm2835 C library
install_py_dependencies:
	sudo pip3 install -r requirements.txt

# only for deploying to remote server (ex. your raspberry pi if you're doing development externally)
deploy_to_mempool:
	rsync --archive --compress --recursive --delete --exclude=build --exclude=*.so --exclude=res/configs.json --exclude=.idea --exclude=env --exclude=var --exclude=__pycache__ --exclude=*.pyc --exclude=tmp --exclude=.git -e "ssh" . pi@192.168.86.61:/home/pi/projects/eth-blockclock

# pre-compile IT8951 libraries
build_app:
	python3 setup.py build_ext --inplace

# run the app (must sudo because we are using bcm2835 C library)
run_app:
	sudo python3 -m eth_blockclock

# install the app as a systemctl service
install_as_service:
	sudo systemctl enable /path/to/your/eth-blockclock/deployment/mempool/eth-blockclock.service && sudo systemctl start eth-blockclock.service
