pipeline {
    agent any

    environment {
        IMAGE_NAME = 'satvikdubey268/gradio-app'
        PYTHON_VERSION = '3.8'
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt pytest
                    pip install --upgrade jinja2>=3.1.2
                    pip install markupsafe==2.0.1
                    
                    python3 -m pytest test.py
                    
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    sudo docker build -t $IMAGE_NAME:latest .
                    sudo docker run -d -p 7860:7860 --name gradio_app $IMAGE_NAME:latest
                '''
            }
        }

        stage('Stop') {
            steps {
                sh '''
                    sudo docker stop gradio_app || true
                    sudo docker rm gradio_app || true
                '''
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline completed.'
        }
    }
}
