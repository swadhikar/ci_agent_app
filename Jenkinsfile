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
        script { // <--- ADD THIS 'script' BLOCK
          def pylintResult = sh(script: 'python3 -m pylint app.py', returnStatus: true)
          if (pylintResult == 0) {
            echo "Pylint passed with exit code 0."
          } else if (pylintResult > 30){
            echo "Pylint failed with unexpected exit code: ${pylintResult}. Marking build as unstable or failing."
            currentBuild.result = 'UNSTABLE'
          } else {
            echo "Pylint completed with conventions/warnings (exit code ${pylintResult}). Allowing pipeline to continue."
          }
        }
      }
    }

    stage('Create and Merge Pull Request') {
      when {
        expression { return env.BRANCH_NAME != 'main' }
      }
      steps {
        script {
          withCredentials([string(credentialsId: 'GITHUB_PAT_FOR_GH_CLI', variable: 'GH_TOKEN')]) {
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
}