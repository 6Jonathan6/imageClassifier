# imageClassifier
This is a project written in python using Django, Postgres as database engine and boto3 to take advantage of several aws services such as S3, rokognition and Cognito.

ImageClassifier allows you  to updload an image to S3 an then aws rekognition analyzes that image afterwards imageClassifier save the json response with the tags on the database an finally shows all the tags from rekognition in a DetailView.

By the way, this project is only backend and does not have any type o frontend framework.
