pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    }

    stages {
        stage('Clone') {
            steps {
                git credentialsId: 'github-creds', url: 'https://github.com/SumantharyaM/aws-devops-3tier-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQube') {
                    withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                        sh '/opt/sonar-scanner/bin/sonar-scanner -Dsonar.login=$SONAR_TOKEN'
                    }
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                dir('backend') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    dockerImage = docker.build("sumantharya/aws-devops-3tier-backend")
                    docker.withRegistry('', 'dockerhub-creds') {
                        dockerImage.push("${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'trivy image --exit-code 0 --severity HIGH,CRITICAL sumantharya/aws-devops-3tier-backend:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }

    post {
        success {
            mail to: 'your@email.com',
                 subject: "SUCCESS: Jenkins Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                 body: "Job succeeded: ${env.BUILD_URL}"
        }

        failure {
            mail to: 'your@email.com',
                 subject: "FAILURE: Jenkins Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                 body: "Job failed: ${env.BUILD_URL}"
        }
    }
}
