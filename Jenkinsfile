pipeline {
  agent {
    kubernetes {
      defaultContainer 'jnlp'
      yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: kaniko
spec:
  serviceAccountName: jenkins-deployer
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  - name: kubectl
    image: bitnami/kubectl:1.32
    command:
    - /bin/sh
    - -c
    - cat
    tty: true
  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-regcred
      items:
      - key: .dockerconfigjson
        path: config.json
'''
    }
  }

  environment {
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

    stage('Build and Push main-app') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context "${WORKSPACE}/services/main-app" \
              --dockerfile "${WORKSPACE}/services/main-app/Dockerfile" \
              --destination "${MAIN_APP_IMAGE}:${IMAGE_TAG}" \
              --destination "${MAIN_APP_IMAGE}:latest"
          '''
        }
      }
    }

    stage('Build and Push news-api') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context "${WORKSPACE}/services/news-api" \
              --dockerfile "${WORKSPACE}/services/news-api/Dockerfile" \
              --destination "${NEWS_API_IMAGE}:${IMAGE_TAG}" \
              --destination "${NEWS_API_IMAGE}:latest"
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        container('kubectl') {
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
}
