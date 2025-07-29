pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    }

    stages {

        stage('Clone') {
            steps {
                git(
                    url: 'https://github.com/SumantharyaM/aws-devops-3tier-app.git',
                    branch: 'main',
                    credentialsId: 'github-creds'
                )
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQube') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                          /opt/sonar-scanner/bin/sonar-scanner \
                            -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }

        stage('Build Backend with Maven') {
            steps {
                dir('backend') {
                    sh 'mvn clean install'
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    sh '''
                    docker build -t sumantharya/backend:latest ./backend
                    docker build -t sumantharya/frontend:latest ./frontend

                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                    docker push sumantharya/backend:latest
                    docker push sumantharya/frontend:latest
                    '''
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'trivy image sumantharya/backend:latest'
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
            mail to: 'sumantharya1@gmail.com',
                 subject: "✅ Build Success",
                 body: "The Jenkins build succeeded and was deployed to EKS."
        }
        failure {
            mail to: 'sumantharya1@gmail.com',
                 subject: "❌ Build Failed",
                 body: "The Jenkins build failed. Please check the logs."
        }
    }
}
