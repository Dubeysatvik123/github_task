pipeline {
    agent any

    environment {
        IMAGE_NAME = 'satvikdubey268/gradio-app'
        PYTHON_VERSION = '3.8'
    }

    stages {
        stage('Test') {
            steps {
                echo '🔍 Running tests...'
                sh '''
                    export PATH=$PATH:/var/lib/jenkins/.local/bin
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt pytest
                    python3 -m pytest test.py -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Building and deploying Docker container...'
                sh '''
                    docker build -t $IMAGE_NAME:latest .
                    docker run -d -p 7860:7860 --name gradio_app $IMAGE_NAME:latest
                '''
            }
        }

        stage('Stop') {
            steps {
                echo '🛑 Stopping Docker container...'
                sh '''
                    docker stop gradio_app || true
                    docker rm gradio_app || true
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
