pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        // Correct way to use SSH credentials with the 'git' step:
        git branch: 'main',
            url: 'git@github.com:swadhikar/ci_agent_app.git',
            credentialsId: 'jenkins-ssh-key'
      }
    }

    stage('Run Unit Tests') {
      steps {
        // Ensure 'pytest' is installed in your Jenkins agent environment
        sh 'pytest test_app.py'
      }
    }

    stage('Auto-Merge to Main') {
      when {
        // This condition correctly checks if the build is for a Pull Request
        expression { env.CHANGE_ID != null }
      }
      steps {
        script {
            echo "This step would contain logic to merge the PR, e.g., using GitHub API."
            echo "Code merge simulated!"
        }
      }
    }
  }
}