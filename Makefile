gen: mainForm.py modify.py
	@echo "done"

%.py : %.ui
	pyuic4 $^ > $@

run: mainForm.py main.py modify.py
	python main.py

.phony:gen run
