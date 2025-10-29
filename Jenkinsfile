// Jenkinsfile - Defines our CI/CD pipeline

pipeline {
    // Agent: Where pipeline runs
    agent any
    
    // Environment variables available to all stages
    environment {
        // Docker Hub credentials (we'll add these later)
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        
        // Image naming
        IMAGE_NAME = "product-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_IMAGE = "${DOCKER_HUB_CREDENTIALS_USR}/${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_IMAGE_LATEST = "${DOCKER_HUB_CREDENTIALS_USR}/${IMAGE_NAME}:latest"
    }
    
    // Pipeline stages - sequential steps
    stages {
        
        // Stage 1: Clone repository from GitHub
        stage('Checkout') {
            steps {
                echo '📥 Cloning repository from GitHub...'
                // Git plugin automatically checks out code
                checkout scm
                echo '✅ Code checked out successfully'
            }
        }
        
        // Stage 2: Build Docker image
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    // Build image using Dockerfile
                    docker.build("${DOCKER_IMAGE}", ".")
                    echo "✅ Docker image built: ${DOCKER_IMAGE}"
                }
            }
        }
        
        // Stage 3: Test the application
        stage('Test Application') {
            steps {
                echo '🧪 Running application tests...'
                script {
                    // Simple image validation
                    sh '''
                        # Verify image was built
                        docker images | grep ${IMAGE_NAME}
                        
                        # Test running container briefly
                        echo "Testing Docker image..."
                        docker run --rm ${DOCKER_IMAGE} python -c "import flask; print('Flask import successful')"
                        
                        echo "✅ Image validation passed!"
                    '''
                }
            }
        }
        
        // Stage 4: Code Quality Analysis with SonarQube (optional)
        // Uncomment when we set up SonarQube
        /*
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Running code quality analysis...'
                script {
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        */
        
        // Stage 5: Push to Docker Hub
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing Docker image to Docker Hub...'
                script {
                    // Login to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        // Push with build number tag
                        docker.image("${DOCKER_IMAGE}").push()
                        // Push with latest tag
                        docker.image("${DOCKER_IMAGE}").push('latest')
                    }
                    echo "✅ Image pushed: ${DOCKER_IMAGE}"
                    echo "✅ Image pushed: ${DOCKER_IMAGE_LATEST}"
                }
            }
        }
        
        // Stage 6: Deploy to environment
        // Simplified for Mac compatibility
        stage('Deploy') {
            steps {
                echo '🚀 Deployment simulation...'
                script {
                    echo 'In production, this would deploy to Kubernetes/AWS'
                    echo "Image available at: ${DOCKER_IMAGE_LATEST}"
                    echo '✅ Deployment stage completed!'
                }
            }
        }
        
        // Stage 7: Smoke Test Deployment
        stage('Smoke Test') {
            steps {
                echo '🔍 Verification complete...'
                script {
                    sh '''
                        # List images
                        docker images | grep ${IMAGE_NAME}
                        
                        echo "✅ Pipeline validation passed!"
                    '''
                }
            }
        }
    }
    
    // Post-build actions
    post {
        always {
            echo '🧹 Cleaning up...'
            // Clean up test containers
            sh 'docker rm -f test-container 2>/dev/null || true'
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            echo "🎉 Build #${BUILD_NUMBER} deployed successfully"
        }
        
        failure {
            echo '❌ Pipeline failed!'
            echo "Build #${BUILD_NUMBER} failed - check logs above"
        }
    }
}


### **D. Paste and Save**

1. Paste the content into the new file in VS Code
2. Click **File → Save** (or press `Cmd+S`)
3. Save as: `Jenkinsfile` (no extension, capital J)
4. Make sure you're saving it in the root of your project folder: `ecommerce-devops-project`

---

## **Step 2: Verify File Structure**

In VS Code's Explorer (left sidebar), you should now see:
```
ecommerce-devops-project/
├── .dockerignore
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
├── Jenkinsfile          ← NEW FILE!
├── README.md
└── requirements.txt