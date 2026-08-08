pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
                bat 'venv\\Scripts\\playwright install'
            }
        }

        stage('Test') {
            steps {
                retry(2) {
                    bat 'venv\\Scripts\\pytest tests --alluredir=reports/allure-report --html=reports/html-report/report.html --self-contained-html'
                }
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    reportName: 'Pytest HTML Report',
                    reportDir: 'reports/html-report',
                    reportFiles: 'report.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: true
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}