#!/bin/bash
while test $# -gt 0; do
    case "$1" in
    --region)
        shift
        export REGION=$1
        shift
        ;;
    --deploy_env)
        shift
        export DEPLOY_ENV=$2
        shift
        ;;
    *)
        echo "$1 is not a recognized flag!"
        return 1
        ;;
    esac
done
if [ -z "$REGION" ]; then
    REGION="eu-central-1"
fi
if [ -z "$DEPLOY_ENV" ]; then
    DEPLOY_ENV="dev"
fi
echo "Region: $REGION"
echo "Environment: $DEPLOY_ENV"
# Clean old keys if they do exist

REGION=$REGION AWS_REGION=$REGION AWS_DEFAULT_REGION=$REGION DEPLOY_ENV=$DEPLOY_ENV cdk deploy --all --force --verbose --region $REGION --require-approval never
if [ $? -eq 0 ]; then
    echo "cdk deploy command was successful."
else
    echo "cdk deploy command failed."
    exit 1
fi