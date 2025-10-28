pipeline {
    agent any

    environment {
        IMAGE_NAME = 'satvikdubey268/gradio-app'
        PYTHON_VERSION = '3.8'
    }

    stages {
        // -------------------- TEST STAGE --------------------
        stage('🧪 Run Unit Tests (pytest)') {
            steps {
                echo 'Running unit tests using pytest...'

                // Checkout source code from Git
                checkout scm

                // Set up Python environment and run tests
                sh '''
                    echo "Setting up Python ${PYTHON_VERSION}"
                    python3 --version || sudo apt install -y python3 python3-pip
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt pytest
                    pytest test.py -v
                '''
            }
        }

        // -------------------- BUILD STAGE --------------------
        stage('🏗️ Build & Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                echo 'Building and pushing Docker image...'

                // Log in to Docker Hub (requires credentials in Jenkins)
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t $IMAGE_NAME:latest .
                        docker tag $IMAGE_NAME:latest $IMAGE_NAME:${BUILD_NUMBER}
                        docker push $IMAGE_NAME:latest
                        docker push $IMAGE_NAME:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed at: ${new Date()}"
        }
        success {
            echo '✅ Build and test successful!'
        }
        failure {
            echo '❌ Pipeline failed. Check console logs.'
        }
    }
}
