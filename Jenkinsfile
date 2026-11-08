pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                bat 'docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.12-slim python test_app.py'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t grade-app:%BUILD_NUMBER% .'
            }
        }

                                stage('Smoke test') {
            steps {
                bat 'docker rm -f grade-test 2>nul || exit /b 0'
                // Change 8085 to 8086 here:
                bat 'docker run -d --name grade-test -p 8086:8080 grade-app:%BUILD_NUMBER%'
                bat 'ping 127.0.0.1 -n 4 > nul'
                // And change 8085 to 8086 here:
                bat 'curl -f http://localhost:8086/health'
            }
            post {
                always {
                    bat 'docker rm -f grade-test'
                }
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker rm -f grade-app 2>nul || exit /b 0'
                bat 'docker run -d --name grade-app -p 8085:8080 grade-app:%BUILD_NUMBER%'
            }
        }
    }

    post {
        success { echo 'Pipeline finished successfully.' }
        failure { echo 'Pipeline failed - see the console output.' }
    }
}
