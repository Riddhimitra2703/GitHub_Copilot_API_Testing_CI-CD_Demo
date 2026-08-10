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
                bat '"C:\\Users\\ACER\\AppData\\Local\\Python\\bin\\python.exe" -m venv venv'
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
                allure([
                    includeProperties: false,
                    jdk: '',
                    commandline: 'Allure_CLI',
                    results: [[path: 'reports/allure-report']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true

            emailext(
                to: 'riddhimitra2003@gmail.com',
                subject: "Build ${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Summary</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> ${currentBuild.currentResult}</p>
                    <p><b>Duration:</b> ${currentBuild.durationString}</p>
                    <p><b>Git Branch:</b> ${env.GIT_BRANCH}</p>
                    <p><b>Git Commit:</b> ${env.GIT_COMMIT}</p>
                    <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><b>Node:</b> ${env.NODE_NAME}</p>
                    <h3>Reports</h3>
                    <p><a href="${env.BUILD_URL}Pytest_20HTML_20Report/">View Pytest HTML Report</a></p>
                    <p><a href="${env.BUILD_URL}allure/">View Allure Report</a></p>
                    <p><a href="${env.BUILD_URL}artifact/">Browse all raw artifacts</a></p>
                    <p><a href="${env.BUILD_URL}console">View full console log</a></p>
                """,
                mimeType: 'text/html'
            )
        }
    }
}
