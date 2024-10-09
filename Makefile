all:
	python3 scripts/ftp_download.py
	python3 scripts/process.py
	
clean:
	find archive/ -maxdepth 1 -name "*.zip" -exec rm -f {} +

.PHONY: clean
