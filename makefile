.DEFAULT_GOAL := install

install:
	@echo "\e[44mInstalling with Poetry\e[0m"
	@poetry install -vvv

black:
	@echo "\e[44mBlack formatting\e[0m"
	@poetry run black hooks/post_gen_project.py
