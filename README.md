# data-monitoring-solution (dms-app)

Data Monitoring Solution (dms-app) is an application designed to simulate signals from a centrifugal pump. With it, it is possible to generate signals and activate and deactivate the signal producer.

### Centrifugal Pump (dms-app)
#### Attributes:
- Maximum operating temperature (°C)
- Minimum head (m.c.a)
- Maximum head (m.c.a)
- Maximum flow (liters/hour)
- Motor voltage (V)
- Discharge diameter (mm)
- Suction diameter (mm)
- Impeller type
- Material of the impeller
- Motor frequency (Hz)
- Current water leak volume (liters)
- Brand of the pump

#### Signal
- Energy consumption in kWh
- Flow rate in liters/hour
- Temperature in °C
- Vibration in Hz
- Water leak volume lost in this moment (liters)

#### Metrics
- Pump Efficiency (Energy per Flow Rate) (Each Minute)
- Pump Vibration Variance (Each Minute)
- Water Leak Rate (Per Pump) (Each Minute)
- Total energy consumption by day
- Pump Temperature vs Vibration Correlation

## Service Infra Architecture (High Level) - TO BE

![DMS drawio](https://github.com/user-attachments/assets/154004df-0276-4e5e-a41b-514ef3b3d92e)


  
## How to execute and install (Application)

### Requirements
- python >= 3.9
- Docker
- Terraform
- Flask
- Helm
- Kubectl
- Git
- Gcloud

1) Clone the repository:
```
git clone https://github.com/egbertosantana/data-monitoring-solution
```
2) Create a virtual machine:
```
python -m venv venv
venv\Scripts\activate
```
3) Install the requirements.txt:
```
pip install -r requirements.txt
```
4) Execute docker-compose
```
docker-compose up -d
```
### Endpoints

1) Start the producer
```
http://127.0.0.1:5000/centrifugal_pump/start
```
2) Stop the producer
```
http://127.0.0.1:5000/centrifugal_pump/stop
```
4) Produce one random register
```
http://127.0.0.1:5000/centrifugal_pump/produce
```
## Deployment

### 1. Terraform Scripts

1) Authenticate to your google account:
```
gcloud auth login
gcloud config set project dms-dev-444818
```

1) Go to the terraform path:
```
cd infra/terraform
```
3) Initialize terraform
```
terraform init
```
4) Contact to get the json about the service account which has permissions and run:
```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```
6) Execute Plan
```
terraform plan -out=tfplan
```
6) Apply Plan
```
terraform apply tfplan
```
### 2. Deploying Application (without Helm)
1) Get the cluster container created by terraform:
```
gcloud container clusters get-credentials dms-dev-app-cluster --region southamerica-east1-a --project dms-dev-444818
```

3) Authetincate Gcloud with docker
```
gcloud auth configure-docker
```

4) Build docker image:
```
docker build -t gcr.io/dms-dev-444818/dms-dev:latest
```

6) Push image:
```
docker push gcr.io/dms-dev-444818/dms-dev:latest
```
6) Apply the deployment and service files:
```
kubectl apply -f infra/deploy/deployment.yaml
kubectl apply -f infra/deploy/service.yaml
```
8) In case if you need to run locally:
```
docker run -it gcr.io/dms-dev-444818/dms-dev:latest
```
### Improvements to the Solution

##### 1. Deliver the entire architecture proposed by the High Level Architecture image
##### 2. Create CI/CD Pipelines (github workflows) for deploying and managing infrastructure as code, the application via helmchart to facilitate the kubernetes deployment process, deployment database migration via liquibase.
##### 3. Create unit tests for infrastructure as code
##### 4. Integrate grafana/prometheus into deployment.
##### 5. Add indexes, caching to the postgres database for performance.
##### 6. Create the secrets manager service for deploying secrets.
##### 7. Create bigquery on GCP to manage high amount of data.
##### 8. Create Cloud composer with airflow to facilitate the execution of services to store and consume data on bigquery.
##### 9. Fix the unit tests that are failing and integrate it into the CI/CD deployment pipeline.
