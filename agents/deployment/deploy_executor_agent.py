
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
import json
from agents.base import BaseAgent

class DeployExecutorAgent(BaseAgent):
    """
    Enhanced deployment agent that generates complete deployment scripts
    for various platforms including Vercel, Netlify, AWS, GCP, and Azure.
    """
    
    def run(self, input_data):
        # Extract parameters
        platform = input_data.get("platform", "vercel")
        project_type = input_data.get("project_type", "next")
        project_path = input_data.get("project_path", ".")
        env_vars = input_data.get("env_vars", {})
        region = input_data.get("region", "us-east-1")
        domain = input_data.get("domain", "")
        
        # Create directory for deployment scripts
        os.makedirs("deployment", exist_ok=True)
        os.makedirs("deployment/scripts", exist_ok=True)
        os.makedirs("deployment/configs", exist_ok=True)
        
        # Generate deployment config
        config = {
            "platform": platform,
            "project_type": project_type,
            "project_path": project_path,
            "env_vars": env_vars,
            "region": region,
            "domain": domain,
            "timestamp": "$(date +%Y%m%d_%H%M%S)"
        }
        
        # Save config file
        with open("deployment/configs/deploy_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        files = {}
        
        # Generate platform-specific files
        if platform.lower() == "vercel":
            # Vercel deployment
            files["deployment/scripts/deploy_vercel.sh"] = self._generate_vercel_script(project_path, env_vars)
            files["deployment/configs/vercel.json"] = self._generate_vercel_config(project_type, env_vars, domain)
            
        elif platform.lower() == "netlify":
            # Netlify deployment
            files["deployment/scripts/deploy_netlify.sh"] = self._generate_netlify_script(project_path)
            files["deployment/configs/netlify.toml"] = self._generate_netlify_config(project_type, env_vars)
            
        elif platform.lower() in ["aws", "amazon"]:
            # AWS deployment
            files["deployment/scripts/deploy_aws.sh"] = self._generate_aws_script(project_path, project_type, region)
            files["deployment/configs/aws_cloudformation.yaml"] = self._generate_aws_cloudformation(project_type, env_vars, domain, region)
            
        elif platform.lower() in ["gcp", "google"]:
            # Google Cloud Platform deployment
            files["deployment/scripts/deploy_gcp.sh"] = self._generate_gcp_script(project_path, project_type)
            files["deployment/configs/app.yaml"] = self._generate_gcp_config(project_type, env_vars)
            
        elif platform.lower() in ["azure", "microsoft"]:
            # Azure deployment
            files["deployment/scripts/deploy_azure.sh"] = self._generate_azure_script(project_path, project_type)
            files["deployment/configs/azure_deploy.json"] = self._generate_azure_config(project_type, env_vars, domain)
            
        else:
            # Generic deployment script
            files["deployment/scripts/deploy_generic.sh"] = self._generate_generic_script(project_path, platform)
        
        # Generate a master deploy script that can handle multiple platforms
        files["deployment/deploy.sh"] = self._generate_master_script(platform)
        
        # Make scripts executable
        for file_path in files:
            if file_path.endswith(".sh"):
                full_path = os.path.join(os.getcwd(), file_path)
                if os.path.exists(full_path):
                    os.chmod(full_path, 0o755)
        
        # Generate README with instructions
        files["deployment/README.md"] = self._generate_deployment_readme(platform, project_type)
        
        return {
            "message": f"Deployment scripts and configurations generated for {platform}.",
            "platform": platform,
            "configs": list(files.keys()),
            "files": files
        }
    
    def _generate_master_script(self, default_platform):
        """Generate a master deployment script that can handle multiple platforms"""
        return f"""#!/bin/bash
# Master deployment script for Sankalpa projects
# This script provides a unified interface for deploying to different platforms

# Load configuration
CONFIG_FILE="deployment/configs/deploy_config.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "Loading configuration from $CONFIG_FILE"
    PLATFORM=$(jq -r '.platform // "{default_platform}"' "$CONFIG_FILE")
    PROJECT_PATH=$(jq -r '.project_path // "."' "$CONFIG_FILE")
else
    echo "No configuration file found. Using defaults."
    PLATFORM="{default_platform}"
    PROJECT_PATH="."
fi

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"

# Command line arguments override configuration
if [ "$1" != "" ]; then
    PLATFORM="$1"
fi

# Check if project exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory $PROJECT_PATH does not exist."
    exit 1
fi

# Display deployment information
echo "===== SANKALPA DEPLOYMENT ====="
echo "Platform: $PLATFORM"
echo "Project directory: $PROJECT_PATH"
echo "=============================="

# Execute platform-specific deployment
case "$PLATFORM" in
    vercel)
        echo "Deploying to Vercel..."
        if [ -f "$SCRIPT_DIR/scripts/deploy_vercel.sh" ]; then
            bash "$SCRIPT_DIR/scripts/deploy_vercel.sh"
        else
            echo "Error: Vercel deployment script not found."
            exit 1
        fi
        ;;
    netlify)
        echo "Deploying to Netlify..."
        if [ -f "$SCRIPT_DIR/scripts/deploy_netlify.sh" ]; then
            bash "$SCRIPT_DIR/scripts/deploy_netlify.sh"
        else
            echo "Error: Netlify deployment script not found."
            exit 1
        fi
        ;;
    aws|amazon)
        echo "Deploying to AWS..."
        if [ -f "$SCRIPT_DIR/scripts/deploy_aws.sh" ]; then
            bash "$SCRIPT_DIR/scripts/deploy_aws.sh"
        else
            echo "Error: AWS deployment script not found."
            exit 1
        fi
        ;;
    gcp|google)
        echo "Deploying to Google Cloud Platform..."
        if [ -f "$SCRIPT_DIR/scripts/deploy_gcp.sh" ]; then
            bash "$SCRIPT_DIR/scripts/deploy_gcp.sh"
        else
            echo "Error: GCP deployment script not found."
            exit 1
        fi
        ;;
    azure|microsoft)
        echo "Deploying to Microsoft Azure..."
        if [ -f "$SCRIPT_DIR/scripts/deploy_azure.sh" ]; then
            bash "$SCRIPT_DIR/scripts/deploy_azure.sh"
        else
            echo "Error: Azure deployment script not found."
            exit 1
        fi
        ;;
    *)
        echo "Error: Unsupported platform '$PLATFORM'"
        echo "Supported platforms: vercel, netlify, aws, gcp, azure"
        exit 1
        ;;
esac

echo "Deployment process completed."
"""
    
    def _generate_vercel_script(self, project_path, env_vars):
        """Generate a Vercel deployment script"""
        env_args = ""
        for key, value in env_vars.items():
            env_args += f"vercel env add {key} production <<< '{value}'\n"
        
        return f"""#!/bin/bash
# Vercel deployment script generated by Sankalpa DeployExecutorAgent
set -e

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# Set environment variables
echo "Setting environment variables..."
{env_args}

# Deploy to production
echo "Deploying to Vercel..."
vercel --prod

echo "Vercel deployment completed successfully!"
"""
    
    def _generate_vercel_config(self, project_type, env_vars, domain):
        """Generate a Vercel configuration file"""
        config = {
            "version": 2,
            "builds": []
        }
        
        if project_type == "next":
            config["builds"] = [
                {
                    "src": "package.json",
                    "use": "@vercel/next"
                }
            ]
        elif project_type == "react":
            config["builds"] = [
                {
                    "src": "package.json",
                    "use": "@vercel/static-build",
                    "config": {
                        "distDir": "build"
                    }
                }
            ]
        elif project_type == "node":
            config["builds"] = [
                {
                    "src": "src/index.js",
                    "use": "@vercel/node"
                }
            ]
        
        # Add routes if domain is specified
        if domain:
            config["routes"] = [
                {
                    "src": "/(.*)",
                    "dest": "/"
                }
            ]
            
            config["crons"] = [
                {
                    "path": "/api/cron",
                    "schedule": "0 0 * * *"
                }
            ]
        
        return json.dumps(config, indent=2)
    
    def _generate_netlify_script(self, project_path):
        """Generate a Netlify deployment script"""
        return f"""#!/bin/bash
# Netlify deployment script generated by Sankalpa DeployExecutorAgent
set -e

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# Deploy to production
echo "Deploying to Netlify..."
netlify deploy --prod

echo "Netlify deployment completed successfully!"
"""
    
    def _generate_netlify_config(self, project_type, env_vars):
        """Generate a Netlify configuration file"""
        build_command = "npm run build"
        publish_directory = "build"
        
        if project_type == "next":
            publish_directory = ".next"
        elif project_type == "gatsby":
            publish_directory = "public"
        
        config = f"""# Netlify configuration file
[build]
  command = "{build_command}"
  publish = "{publish_directory}"

# Environment variables
[build.environment]
"""
        
        for key, value in env_vars.items():
            config += f"  {key} = \"{value}\"\n"
        
        return config
    
    def _generate_aws_script(self, project_path, project_type, region):
        """Generate an AWS deployment script"""
        return f"""#!/bin/bash
# AWS deployment script generated by Sankalpa DeployExecutorAgent
set -e

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI not found. Please install it first."
    exit 1
fi

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# Create S3 bucket if it doesn't exist
BUCKET_NAME="sankalpa-deployment-$(date +%Y%m%d)"
echo "Creating/checking S3 bucket: $BUCKET_NAME"
aws s3 mb s3://$BUCKET_NAME --region {region} || true

# Upload CloudFormation template
echo "Uploading CloudFormation template..."
aws s3 cp deployment/configs/aws_cloudformation.yaml s3://$BUCKET_NAME/

# Package application
echo "Packaging application..."
if [ "{project_type}" == "next" ] || [ "{project_type}" == "react" ]; then
    # For frontend apps, zip the build directory
    BUILD_DIR=$([ "{project_type}" == "next" ] && echo ".next" || echo "build")
    zip -r deployment/app.zip $BUILD_DIR
else
    # For Node.js apps, zip everything except node_modules
    zip -r deployment/app.zip . -x "node_modules/*"
fi

# Upload application package
echo "Uploading application package..."
aws s3 cp deployment/app.zip s3://$BUCKET_NAME/

# Deploy with CloudFormation
STACK_NAME="sankalpa-stack-$(date +%Y%m%d)"
echo "Deploying CloudFormation stack: $STACK_NAME"
aws cloudformation create-stack \\
    --stack-name $STACK_NAME \\
    --template-url https://$BUCKET_NAME.s3.amazonaws.com/aws_cloudformation.yaml \\
    --capabilities CAPABILITY_IAM \\
    --parameters ParameterKey=BucketName,ParameterValue=$BUCKET_NAME \\
                ParameterKey=ProjectType,ParameterValue={project_type}

echo "Waiting for stack creation to complete..."
aws cloudformation wait stack-create-complete --stack-name $STACK_NAME

# Output the deployed URL
echo "Deployment completed. Outputs:"
aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs"
"""
    
    def _generate_aws_cloudformation(self, project_type, env_vars, domain, region):
        """Generate an AWS CloudFormation template"""
        if project_type in ["next", "react", "vue"]:
            # Frontend deployment with S3 and CloudFront
            template = """
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Sankalpa Frontend Deployment with S3 and CloudFront'

Parameters:
  BucketName:
    Type: String
    Description: Name of the S3 bucket for deployment
  ProjectType:
    Type: String
    Description: Type of project being deployed
    Default: next
    AllowedValues:
      - next
      - react
      - vue

Resources:
  WebsiteBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      AccessControl: PublicRead
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: error.html

  WebsiteBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref WebsiteBucket
      PolicyDocument:
        Statement:
          - Effect: Allow
            Principal: '*'
            Action: 's3:GetObject'
            Resource: !Join ['', ['arn:aws:s3:::', !Ref WebsiteBucket, '/*']]

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - DomainName: !GetAtt WebsiteBucket.DomainName
            Id: S3Origin
            CustomOriginConfig:
              OriginProtocolPolicy: http-only
        Enabled: true
        DefaultRootObject: index.html
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          ViewerProtocolPolicy: redirect-to-https
        ViewerCertificate:
          CloudFrontDefaultCertificate: true

Outputs:
  WebsiteURL:
    Description: URL for the S3 website
    Value: !GetAtt WebsiteBucket.WebsiteURL
  CloudFrontURL:
    Description: URL for the CloudFront distribution
    Value: !Join ['', ['https://', !GetAtt CloudFrontDistribution.DomainName]]
"""
        else:
            # Backend deployment with Elastic Beanstalk
            template = """
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Sankalpa Backend Deployment with Elastic Beanstalk'

Parameters:
  BucketName:
    Type: String
    Description: Name of the S3 bucket for deployment artifacts
  ProjectType:
    Type: String
    Description: Type of project being deployed
    Default: node
    AllowedValues:
      - node
      - express
      - fastapi
      - django

Resources:
  ElasticBeanstalkApplication:
    Type: AWS::ElasticBeanstalk::Application
    Properties:
      ApplicationName: SankalpaApplication

  ApplicationVersion:
    Type: AWS::ElasticBeanstalk::ApplicationVersion
    Properties:
      ApplicationName: !Ref ElasticBeanstalkApplication
      SourceBundle:
        S3Bucket: !Ref BucketName
        S3Key: app.zip

  ElasticBeanstalkEnvironment:
    Type: AWS::ElasticBeanstalk::Environment
    Properties:
      ApplicationName: !Ref ElasticBeanstalkApplication
      EnvironmentName: SankalpaProduction
      SolutionStackName: "64bit Amazon Linux 2 v5.8.0 running Node.js 16"
      VersionLabel: !Ref ApplicationVersion
      OptionSettings:
        - Namespace: aws:autoscaling:launchconfiguration
          OptionName: InstanceType
          Value: t2.micro
        - Namespace: aws:elasticbeanstalk:environment
          OptionName: EnvironmentType
          Value: SingleInstance

Outputs:
  EnvironmentURL:
    Description: URL of the Elastic Beanstalk environment
    Value: !GetAtt ElasticBeanstalkEnvironment.EndpointURL
"""
        
        return template
    
    def _generate_gcp_script(self, project_path, project_type):
        """Generate a Google Cloud Platform deployment script"""
        return f"""#!/bin/bash
# Google Cloud Platform deployment script generated by Sankalpa DeployExecutorAgent
set -e

# Check if Google Cloud SDK is installed
if ! command -v gcloud &> /dev/null; then
    echo "Google Cloud SDK not found. Please install it first."
    exit 1
fi

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# Set up Google Cloud project
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "No Google Cloud project selected. Please run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit 1
fi

echo "Deploying to Google Cloud project: $PROJECT_ID"

# Deploy based on project type
if [ "{project_type}" == "next" ] || [ "{project_type}" == "react" ]; then
    # Deploy frontend to Firebase Hosting
    echo "Deploying frontend to Firebase Hosting..."
    
    # Check if Firebase CLI is installed
    if ! command -v firebase &> /dev/null; then
        echo "Firebase CLI not found. Installing..."
        npm install -g firebase-tools
    fi
    
    # Initialize Firebase if needed
    if [ ! -f "firebase.json" ]; then
        echo "Initializing Firebase..."
        firebase init hosting
    fi
    
    # Deploy to Firebase
    firebase deploy --only hosting
else
    # Deploy backend to App Engine
    echo "Deploying backend to App Engine..."
    gcloud app deploy deployment/configs/app.yaml
fi

echo "Google Cloud deployment completed successfully!"
"""
    
    def _generate_gcp_config(self, project_type, env_vars):
        """Generate a Google Cloud Platform App Engine configuration"""
        if project_type in ["node", "express"]:
            config = """runtime: nodejs16

env: standard
instance_class: F1

handlers:
  - url: /.*
    script: auto

env_variables:
"""
            for key, value in env_vars.items():
                config += f"  {key}: '{value}'\n"
        else:
            config = """runtime: python39

env: standard
instance_class: F1

handlers:
  - url: /.*
    script: auto

env_variables:
"""
            for key, value in env_vars.items():
                config += f"  {key}: '{value}'\n"
        
        return config
    
    def _generate_azure_script(self, project_path, project_type):
        """Generate an Azure deployment script"""
        return f"""#!/bin/bash
# Microsoft Azure deployment script generated by Sankalpa DeployExecutorAgent
set -e

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI not found. Please install it first."
    exit 1
fi

# Check if logged in to Azure
az account show &> /dev/null
if [ $? -ne 0 ]; then
    echo "Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# Create resource group if it doesn't exist
RESOURCE_GROUP="sankalpa-rg"
echo "Creating/checking resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location eastus

# Deploy based on project type
if [ "{project_type}" == "next" ] || [ "{project_type}" == "react" ]; then
    # Deploy frontend to Azure Static Web Apps
    echo "Deploying frontend to Azure Static Web Apps..."
    
    APP_NAME="sankalpa-static-webapp"
    OUTPUT_DIR=$([ "{project_type}" == "next" ] && echo ".next" || echo "build")
    
    az staticwebapp create \\
        --name $APP_NAME \\
        --resource-group $RESOURCE_GROUP \\
        --source . \\
        --location "eastus2" \\
        --output-location $OUTPUT_DIR \\
        --branch main
else
    # Deploy backend to Azure App Service
    echo "Deploying backend to Azure App Service..."
    
    APP_NAME="sankalpa-app-service"
    
    # Create App Service plan
    az appservice plan create \\
        --name sankalpa-app-plan \\
        --resource-group $RESOURCE_GROUP \\
        --sku B1 \\
        --is-linux
    
    # Create Web App
    az webapp create \\
        --name $APP_NAME \\
        --resource-group $RESOURCE_GROUP \\
        --plan sankalpa-app-plan \\
        --runtime "NODE|16-lts"
    
    # Deploy code
    az webapp deploy \\
        --resource-group $RESOURCE_GROUP \\
        --name $APP_NAME \\
        --src-path . \\
        --type zip
    
    # Set environment variables
    for key in $(jq -r '.env_vars | keys[]' deployment/configs/deploy_config.json); do
        value=$(jq -r ".env_vars.$key" deployment/configs/deploy_config.json)
        az webapp config appsettings set \\
            --resource-group $RESOURCE_GROUP \\
            --name $APP_NAME \\
            --settings "$key=$value"
    done
fi

echo "Azure deployment completed successfully!"
"""
    
    def _generate_azure_config(self, project_type, env_vars, domain):
        """Generate an Azure ARM template configuration"""
        # This is a simplified Azure ARM template
        template = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "appName": {
                    "type": "string",
                    "defaultValue": "sankalpa-app",
                    "metadata": {
                        "description": "The name of the app service"
                    }
                }
            },
            "variables": {
                "location": "[resourceGroup().location]",
                "appServicePlanName": "[concat(parameters('appName'), '-plan')]"
            },
            "resources": [
                {
                    "type": "Microsoft.Web/serverfarms",
                    "apiVersion": "2020-06-01",
                    "name": "[variables('appServicePlanName')]",
                    "location": "[variables('location')]",
                    "sku": {
                        "name": "B1",
                        "tier": "Basic"
                    },
                    "properties": {
                        "reserved": True
                    }
                },
                {
                    "type": "Microsoft.Web/sites",
                    "apiVersion": "2020-06-01",
                    "name": "[parameters('appName')]",
                    "location": "[variables('location')]",
                    "dependsOn": [
                        "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]"
                    ],
                    "properties": {
                        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
                        "siteConfig": {
                            "linuxFxVersion": "NODE|16-lts",
                            "appSettings": []
                        }
                    }
                }
            ],
            "outputs": {
                "appServiceUrl": {
                    "type": "string",
                    "value": "[concat('https://', parameters('appName'), '.azurewebsites.net')]"
                }
            }
        }
        
        # Add environment variables to app settings
        app_settings = []
        for key, value in env_vars.items():
            app_settings.append({
                "name": key,
                "value": value
            })
        
        if app_settings:
            template["resources"][1]["properties"]["siteConfig"]["appSettings"] = app_settings
        
        return json.dumps(template, indent=2)
    
    def _generate_generic_script(self, project_path, platform):
        """Generate a generic deployment script template"""
        return f"""#!/bin/bash
# Generic deployment script for {platform} generated by Sankalpa DeployExecutorAgent
set -e

# Navigate to project directory
cd {project_path}

# Install dependencies
echo "Installing dependencies..."
npm install

# Build the project
echo "Building project..."
npm run build

# TODO: Add specific deployment commands for {platform}
# This is a template that you should customize for your specific platform

echo "Deployment to {platform} completed successfully!"
"""
    
    def _generate_deployment_readme(self, platform, project_type):
        """Generate a README file with deployment instructions"""
        
        instructions = f"""# Deployment Guide for {platform.title()}

This folder contains all the necessary scripts and configurations to deploy your {project_type} project to {platform.title()}.

## Prerequisites

"""
        
        if platform.lower() == "vercel":
            instructions += """- Node.js and npm installed
- Vercel CLI installed (`npm install -g vercel`)
- Vercel account and logged in via CLI (`vercel login`)

## Deployment Steps

1. Navigate to this directory: `cd deployment`
2. Run the deployment script: `./deploy.sh`
3. The script will:
   - Install dependencies
   - Build the project
   - Set environment variables
   - Deploy to Vercel

## Configuration

You can modify the deployment configuration in `configs/deploy_config.json`.

## Custom Domain

To set up a custom domain:
1. Go to your Vercel project dashboard
2. Click on "Domains"
3. Add your domain and follow the instructions

## Environment Variables

Environment variables are stored in the config file and will be automatically set during deployment.
"""
        
        elif platform.lower() == "netlify":
            instructions += """- Node.js and npm installed
- Netlify CLI installed (`npm install -g netlify-cli`)
- Netlify account and logged in via CLI (`netlify login`)

## Deployment Steps

1. Navigate to this directory: `cd deployment`
2. Run the deployment script: `./deploy.sh`
3. The script will:
   - Install dependencies
   - Build the project
   - Deploy to Netlify

## Configuration

You can modify the Netlify configuration in `configs/netlify.toml`.

## Custom Domain

To set up a custom domain:
1. Go to your Netlify project dashboard
2. Click on "Domain settings"
3. Click on "Add custom domain"
4. Follow the instructions

## Environment Variables

Environment variables are defined in the Netlify configuration file and will be automatically set during deployment.
"""
        
        elif platform.lower() in ["aws", "amazon"]:
            instructions += """- AWS CLI installed and configured (`aws configure`)
- AWS account with appropriate permissions
- Node.js and npm installed

## Deployment Steps

1. Navigate to this directory: `cd deployment`
2. Run the deployment script: `./deploy.sh`
3. The script will:
   - Create necessary S3 buckets
   - Build the project
   - Package the application
   - Deploy using CloudFormation

## Configuration

You can modify the AWS CloudFormation template in `configs/aws_cloudformation.yaml`.

## Custom Domain

To set up a custom domain with AWS:
1. Register a domain in Route 53 or use an existing domain
2. Create an SSL certificate in AWS Certificate Manager
3. Update the CloudFormation template to include the domain configuration
4. Redeploy

## Environment Variables

Environment variables are defined in the CloudFormation template and will be set during deployment.
"""
        
        elif platform.lower() in ["gcp", "google"]:
            instructions += """- Google Cloud SDK installed and configured
- GCP project created and selected (`gcloud config set project YOUR_PROJECT_ID`)
- Node.js and npm installed
- For frontend projects: Firebase CLI installed (`npm install -g firebase-tools`)

## Deployment Steps

1. Navigate to this directory: `cd deployment`
2. Run the deployment script: `./deploy.sh`
3. The script will:
   - Build the project
   - Deploy to App Engine (backend) or Firebase Hosting (frontend)

## Configuration

You can modify the App Engine configuration in `configs/app.yaml`.

## Custom Domain

To set up a custom domain with GCP:
1. For App Engine:
   - Go to the App Engine dashboard
   - Click on "Settings" > "Custom domains"
   - Follow the instructions to map your domain
2. For Firebase Hosting:
   - Go to the Firebase Hosting dashboard
   - Click on "Connect domain"
   - Follow the instructions

## Environment Variables

Environment variables are defined in the App Engine configuration file and will be set during deployment.
"""
        
        elif platform.lower() in ["azure", "microsoft"]:
            instructions += """- Azure CLI installed and configured (`az login`)
- Azure account with appropriate subscription
- Node.js and npm installed

## Deployment Steps

1. Navigate to this directory: `cd deployment`
2. Run the deployment script: `./deploy.sh`
3. The script will:
   - Create necessary Azure resources
   - Build the project
   - Deploy to Azure Static Web Apps (frontend) or Azure App Service (backend)

## Configuration

You can modify the Azure ARM template in `configs/azure_deploy.json`.

## Custom Domain

To set up a custom domain with Azure:
1. For App Service:
   - Go to your App Service in the Azure portal
   - Click on "Custom domains"
   - Follow the instructions to add your domain
2. For Static Web Apps:
   - Go to your Static Web App in the Azure portal
   - Click on "Custom domains"
   - Follow the instructions

## Environment Variables

Environment variables are defined in the ARM template and will be set during deployment.
"""
        
        return instructions