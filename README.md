# LSML2
## LSML2 final project by Damir Khabibulin 08.09.2021

Dataset: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html

Project goals: Create an ML-service to solve any kind of task.

### Architecture:
- Model: trained on iris dataset XGBClassifier model

### Containers:
1) app: Flask web server to serve simple web interface
2) celery: Celery worker to asynchronously serve model
3) redis: For storing celery tasks
4) mlflow: MLFlow for tracking models
5) db: Database server for mlflow

### Installing:
1) Docker https://docs.docker.com/engine/install/
2) Docker compose https://docs.docker.com/compose/install/
4) To train model run: `pip install -r requirements.txt`, then `python train.py`

### Running:
`sudo docker-compose up --build`

##### Web interface:
User Interface - `http://localhost:9091/`
MLFLow web interface - `http://127.0.0.1:5000/#/`
