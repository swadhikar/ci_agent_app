pipeline {
  agent any

  environment {
    GITHUB_TOKEN = credentials('jenkins-cicd') // stored in Jenkins Credentials
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/swadhikar/ci_agent_app'
      }
    }

    stage('Run Unit Tests') {
      steps {
        sh 'pytest test_app.py'
      }
    }

    stage('Merge PR if Passed') {
      when {
        expression { env.CHANGE_ID != null }  // Only if this is a PR
      }
      steps {
        script {
            echo "Code merge simulated!"
        //   sh """
        //   curl -X PUT \
        //     -H "Authorization: token ${GITHUB_TOKEN}" \
        //     -H "Accept: application/vnd.github+json" \
        //     https://api.github.com/repos/swadhikar/ci_agent_app/pulls/${env.CHANGE_ID}/merge
        //   """
        }
      }
    }
  }
}
