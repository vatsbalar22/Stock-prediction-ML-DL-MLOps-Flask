install : 
	pip install --upgrade pip &&\
		pip install -r requirements.txt
# test:
# 	python -m pytest -vv app.py

lint:
	pylint --disable=R,C,W0621,W0612,W0611,W0632,W0621 *.py
	
# format:
# 	black *.py nlplogic

all: install lint  		
