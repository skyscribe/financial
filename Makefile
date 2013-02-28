gen: mainForm.py modify.py
	@echo "done"

%.py : %.ui
	pyuic4 $^ > $@

run: mainForm.py main.py modify.py
	python main.py

pkg: gen
	cxfreeze --target-dir=dist --include-modules=sip,encodings.ascii,encodings.hex_codec,encodings.utf_8 main.py

.phony:gen run
