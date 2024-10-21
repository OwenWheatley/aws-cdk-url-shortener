import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_url_shortener.aws_cdk_url_shortener_stack import AwsCdkUrlShortenerStack

def test_dynamodb_table_created():
    app = core.App()
    stack = AwsCdkUrlShortenerStack(app, "AwsCdkUrlShortenerStack")
    
    # Create the CloudFormation template for the stack
    template = assertions.Template.from_stack(stack)

    # Check if a DynamoDB table is created
    template.has_resource_properties("AWS::DynamoDB::Table", {
        "KeySchema": [{
            "AttributeName": "shortUrl",
            "KeyType": "HASH"
        }]
    })

def test_lambda_function_created():
    app = core.App()
    stack = AwsCdkUrlShortenerStack(app, "AwsCdkUrlShortenerStack")
    
    # Create the CloudFormation template for the stack
    template = assertions.Template.from_stack(stack)

    # Check if a Lambda function is created with the correct runtime
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "aws_cdk_url_shortener.handler",
        "Runtime": "python3.9"
    })

def test_api_gateway_created():
    app = core.App()
    stack = AwsCdkUrlShortenerStack(app, "AwsCdkUrlShortenerStack")
    
    # Create the CloudFormation template for the stack
    template = assertions.Template.from_stack(stack)

    # Check if an API Gateway REST API is created
    template.resource_count_is("AWS::ApiGateway::RestApi", 1)

def test_lambda_has_correct_permissions():
    app = core.App()
    stack = AwsCdkUrlShortenerStack(app, "AwsCdkUrlShortenerStack")
    
    # Create the CloudFormation template for the stack
    template = assertions.Template.from_stack(stack)

    # Check if the Lambda function has the required IAM policy for DynamoDB
    template.has_resource_properties("AWS::IAM::Policy", {
        "PolicyDocument": {
            "Statement": [{
                "Action": [
                    "dynamodb:BatchGetItem",
                    "dynamodb:GetRecords",
                    "dynamodb:GetShardIterator",
                    "dynamodb:Query",
                    "dynamodb:GetItem",
                    "dynamodb:Scan",
                    "dynamodb:ConditionCheckItem",
                    "dynamodb:BatchWriteItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                    "dynamodb:DescribeTable"
                ],
                "Effect": "Allow"
            }]
        }
    })


