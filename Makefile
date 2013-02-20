gen: mainForm.py
	@echo "done"

mainForm.py : mainForm.ui
	pyuic4 $^ > $@

run: mainForm.py main.py
	python main.py

.phony:gen run
