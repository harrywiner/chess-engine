.PHONY: test

test:
	python3 main.py --entrypoint=test

play:
	python3 main.py $(if $(DEPTH),--depth=$(DEPTH))