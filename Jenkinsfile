pipeline {
  agent any

  environment {
    DOCKERHUB_USERNAME = 'zurang'
    MAIN_APP_IMAGE = 'zurang/main-app'
    NEWS_API_IMAGE = 'zurang/news-api'
    IMAGE_TAG = "${BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Main App Image') {
      steps {
        dir('services/main-app') {
          sh 'docker build -t ${MAIN_APP_IMAGE}:${IMAGE_TAG} -t ${MAIN_APP_IMAGE}:latest .'
        }
      }
    }

    stage('Build News API Image') {
      steps {
        dir('services/news-api') {
          sh 'docker build -t ${NEWS_API_IMAGE}:${IMAGE_TAG} -t ${NEWS_API_IMAGE}:latest .'
        }
      }
    }

    stage('DockerHub Login') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
        }
      }
    }

    stage('Push Images') {
      steps {
        sh 'docker push ${MAIN_APP_IMAGE}:${IMAGE_TAG}'
        sh 'docker push ${MAIN_APP_IMAGE}:latest'
        sh 'docker push ${NEWS_API_IMAGE}:${IMAGE_TAG}'
        sh 'docker push ${NEWS_API_IMAGE}:latest'
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl -n app set image deployment/main-app main-app=${MAIN_APP_IMAGE}:latest
          kubectl -n app set image deployment/news-api news-api=${NEWS_API_IMAGE}:latest
          kubectl -n app rollout status deployment/main-app --timeout=180s
          kubectl -n app rollout status deployment/news-api --timeout=180s
        '''
      }
    }
  }
}
