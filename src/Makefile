SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

PYTHON = python.exe

.PHONY: proxy publisher subscriber put get sub unsub clean

RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(RUN_ARGS):;@:)

# Run Proxy
proxy:
	@$(PYTHON) proxy_run.py

# Run a publisher
publisher:
	@$(PYTHON) pub_run.py $(filter-out $@, $(MAKECMDGOALS))


# Create a node in the network
node:
	@$(PYTHON) node.py $@ $(RUN_ARGS)

node1:
	@$(PYTHON) node.py -i 127.0.0.1 -p 8001 -b True

node2:
	@$(PYTHON) node.py -i 127.0.0.1 -p 8002

node3:
	@$(PYTHON) node.py -i 127.0.0.1 -p 8003


# Set message
set:
	@$(PYTHON) set.py $@ $(RUN_ARGS)

set1:
	@$(PYTHON) set.py 127.0.0.1 8001 topic-1 message-1

set2:
	@$(PYTHON) set.py 127.0.0.1 8001 topic-1 message-2

set3:
	@$(PYTHON) set.py 127.0.0.1 8002 topic-2 message-3

# Get message
get:
	@$(PYTHON) get.py $@ $(RUN_ARGS)

get1:
	@$(PYTHON) get.py 127.0.0.1 8001 topic-1

get2:
	@$(PYTHON) get.py 127.0.0.1 8002 topic-1

get3:
	@$(PYTHON) get.py 127.0.0.1 8001 topic-2

get4:
	@$(PYTHON) get.py 127.0.0.1 8002 topic-2

