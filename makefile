install : 
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	pylint --disable=R,C,W0621,W0612,W0611,W0632,W0621 *.py

run:
	python train_model.py
		python predict_model.py
			python app.py
s_run:
	streamlit run s_app.py

all: install lint run   		
