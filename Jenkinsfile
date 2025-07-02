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

    stage('Run Static Code analysis') {
      steps {
        sh 'pytest test_app.py'
      }
    }

    stage('Run Unit Tests') {
      steps {
        sh 'python3 -m pylint test_app.py'
      }
    }

    stage('Create and Merge Pull Request') {
      when {
        expression { return env.BRANCH_NAME != 'main' }
      }
      steps {
        script {
          // Check if PR already exists for this branch
          def prNumber = sh(
            script: """
              gh pr list --state open --head ${env.BRANCH_NAME} --json number --jq '.[0].number'
            """,
            returnStdout: true
          ).trim()

          if (prNumber) {
            echo "PR already exists: #${prNumber}"
          } else {
            echo "Creating PR from ${env.BRANCH_NAME} to main..."
            prNumber = sh(
              script: """
                gh pr create --base main --head ${env.BRANCH_NAME} \
                  --title "Auto PR from Jenkins: ${env.BRANCH_NAME}" \
                  --body "Auto-created PR after passing lint and unit tests." \
                  --json number --jq '.number'
              """,
              returnStdout: true
            ).trim()
            echo "Created PR: #${prNumber}"
          }

          // Auto-merge the PR
          echo "Attempting to auto-merge PR #${prNumber}"
          sh """
            gh pr merge ${prNumber} --merge \
              --subject "Pylint and UT complete" \
              --body "This PR was auto-merged by Jenkins after all checks passed."
          """
          echo "Auto-merge complete"
        }
      }
    }
  }
}