pipeline {
    agent any
    environment {
        GITHUB_CREDENTIALS = credentials('github-creds-id')
        DOCKERHUB_CREDS = credentials('dockerhub-creds-id')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/s-shemmee/alx-backend-python.git', credentialsId: "${GITHUB_CREDENTIALS}"
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t s-shemmee/messaging-app:latest .'
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "dockerhub-creds-id", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push s-shemmee/messaging-app:latest'
                }
            }
        }
    }
}