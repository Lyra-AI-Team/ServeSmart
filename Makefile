install:
	pip install -r requirements.txt

run:
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

docker-build:
	docker build -t myapp .

docker-run:
	docker run -p 8501:8501 myapp

docker-clean:
	docker rmi myapp
