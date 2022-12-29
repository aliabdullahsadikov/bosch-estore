pipeline {

//     agent  { docker { image 'python:3'} }
    agent any
    environment {
        ENV = 'dev'
    }

    stages {
        stage('Setup') {
            steps{
                echo "Setup"
            }
        }

        stage('Build') {
            agent {
                alembic
            }
            steps {
                echo "Build"
                sh 'pip3 install -r requirements.txt'
                echo "Hello"
            }
        }
    }
}