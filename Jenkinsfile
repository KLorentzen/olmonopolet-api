pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
            }
        }
        stage('Test') {
            steps {
                echo "Test stage..."
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploy stage..."
            }
        }
    }
}