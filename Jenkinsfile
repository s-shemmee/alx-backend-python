pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }
    environment {
        GITHUB_CREDENTIALS = credentials('github-creds-id')
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
    }
}