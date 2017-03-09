init:
	pyenv install 3.4.6
	pyenv virtualenv poker_math_env34
	pyenv local poker_math_env34

dep:
	pip install -r requirements.txt

updatedep:
	pip freeze > requirements.txt

.PHONY: init dep updatedep
