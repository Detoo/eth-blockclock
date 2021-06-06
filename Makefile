help:
	@egrep '^\w+:' Makefile

# must sudo because so far we are still using bcm2835 C library
install_py_dependencies:
	sudo pip3 install -r requirements.txt

deploy_to_mempool:
	rsync --archive --compress --recursive --delete --exclude=build --exclude=*.so --exclude=.idea --exclude=env --exclude=var --exclude=__pycache__ --exclude=*.pyc --exclude=tmp --exclude=.git -e "ssh" . pi@192.168.86.61:/home/pi/projects/eth-blockclock

build_app:
	python3 setup.py build_ext --inplace

run_app:
	sudo python3 -m eth_blockclock
