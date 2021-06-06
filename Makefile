help:
	@egrep '^\w+:' Makefile

deploy_to_mempool:
	rsync --archive --compress --recursive --delete --exclude=.idea --exclude=env --exclude=var --exclude==__pycache__ --exclude=*.pyc --exclude=tmp --exclude=.git -e "ssh" . pi@192.168.86.61:/home/pi/projects/eth-blockclock
