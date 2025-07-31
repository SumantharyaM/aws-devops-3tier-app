pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        AWS_CREDS = credentials('aws-creds') // single AWS credential block with both access key and secret
    }

    stages {

        stage('Clone Repository') {
            steps {
                git(
                    url: 'https://github.com/SumantharyaM/aws-devops-3tier-app.git',
                    branch: 'main',
                    credentialsId: 'github-creds'
                )
            }
        }

        stage('SonarQube Code Analysis') {
            environment {
                SONAR_TOKEN = credentials('sonar-token')
            }
            steps {
                withSonarQubeEnv('MySonarQube') {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                      -Dsonar.projectKey=aws-devops-3tier \
                      -Dsonar.sources=. \
                      -Dsonar.exclusions=backend/venv/**/* \
                      -Dsonar.host.url=http://localhost:9000 \
                      -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Install Backend Python Dependencies') {
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

        stage('Trivy Image Scan') {
            steps {
                sh '''
                trivy image sumantharya/backend:latest || true
                trivy image sumantharya/frontend:latest || true
                '''
            }
        }

        stage('Deploy to Kubernetes (EKS)') {
            environment {
                AWS_ACCESS_KEY_ID = "${AWS_CREDS_USR}"
                AWS_SECRET_ACCESS_KEY = "${AWS_CREDS_PSW}"
                AWS_DEFAULT_REGION = "ap-south-1"
            }
            steps {
                sh '''
                aws eks update-kubeconfig --region $AWS_DEFAULT_REGION --name devops-cluster
                kubectl apply -f k8s/ --validate=false
                '''
            }
        }
    }

    post {
        success {
            mail to: 'sumantharya1@gmail.com',
                 subject: "✅ Build Success - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "🎉 Jenkins build succeeded and deployed to EKS.\nCheck logs: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'sumantharya1@gmail.com',
                 subject: "❌ Build Failed - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "🚨 Jenkins build failed.\nCheck logs: ${env.BUILD_URL}"
        }
    }
}
