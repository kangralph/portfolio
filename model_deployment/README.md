# Model Deployment Sample for GCP AI Platform

  

## Steps:

  

1. Train your model and save model as a joblib file: 
```bash
	python train.py
```

2. Create a package for your custom code:
```bash
	python setup.py sdist --formats gztar
```

3. Copy your package and joblib files to GCP Cloud Storage:
``` bash
	gsutil cp dist/custom_code-0.1.tar.gz gs://$BUCKET_NAME//custom_code-0.1.tar.gz
	gsutil -m cp *.joblib gs://BUCKET_NAME
```

> Note you need to have proper credentials to gain access to GCP locally

4. Deploy to existing model on AI Platform via Cloud Shell:
> Set your env variables 
```bash
	MODEL_DIR="gs://"$BUCKET_NAME
	VERSION_NAME="v0"  
	MODEL_NAME="your_model"  
	CUSTOM_CODE_PATH="gs://"$BUCKET_NAME"/custom_code-0.1.tar.gz"  
	PREDICTOR_CLASS="custom_prediction.YourPredictor"
```

> Create Version off your existing Model
```bash
gcloud beta ai-platform versions create $VERSION_NAME \
	--model $MODEL_NAME \
	--origin $MODEL_DIR \
	--runtime-version=2.2 \
	--python-version=3.7 \
	--package-uris=$CUSTOM_CODE_PATH \
	--prediction-class=$PREDICTOR_CLASS
```

> Test your model if it serves predictions
```bash
gcloud ai-platform predict --model $MODEL_NAME --version $VERSION_NAME --json-instances $JSON_FILE
```