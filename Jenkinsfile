
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'satvikdubey268/gradio-app'
        PYTHON_VERSION = '3.8'
    }

    stages {
        stage('Test') {
            steps {
                echo 'Running tests...'
                // checkout scm
                // sh '''
                //     python3 -m pip install --upgrade pip
                //     pip install -r requirements.txt 
                //     pip install pytest
                //     pytest test.py -v
                // '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t $IMAGE_NAME:latest .
                    docker run -p 7860:7860 $IMAGE_NAME:latest
                '''
            }
        }
    }
}
