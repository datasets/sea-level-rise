all:
	python2 scripts/process.py

clean:
	rm data/* archive/*

.PHONY: clean
