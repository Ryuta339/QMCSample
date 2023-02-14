#!/bin/sh

if [ $1 == 'up' ]; then
	docker-compose up -d
	sleep 1; open http://localhost:8888/lab/tree/work
elif [ $1 == 'down' ]; then
	docker-compose down
fi
