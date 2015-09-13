# Makefile for surveyor

# ----------------------------------------------------------------------------

ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# ----------------------------------------------------------------------------

all: tox

# ----------------------------------------------------------------------------

tox:
	cd $(ROOT_DIR) && tox

test:
	cd $(ROOT_DIR) && py.test

clean:
	rm -rf $(ROOT_DIR)/.tox && \
	rm -rf $(ROOT_DIR)/.cache && \
	rm -rf $(ROOT_DIR)/build && \
	rm -rf $(ROOT_DIR)/dist && \
	rm -rf $(ROOT_DIR)/*.egg-info && \
	rm -f $(ROOT_DIR)/.coverage && \
	find . -name "*.py[co]" -type f -delete && \
	find . -name "__pycache__" -type d -delete
