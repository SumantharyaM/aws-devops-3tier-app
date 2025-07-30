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
            environment {
                SONAR_TOKEN = credentials('sonar-token') // Store token as secret text
            }
            steps {
                withSonarQubeEnv('MySonarQube') {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                      -Dsonar.projectKey=aws-devops-3tier \
                      -Dsonar.sources=. \
                      -Dsonar.host.url=http://localhost:9000 \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                dir('backend') {
                    sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
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
