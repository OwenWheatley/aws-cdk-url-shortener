from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class AwsCdkUrlShortenerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #DynamoDB Table to store URLs
        table = dynamodb.Table(self, "UrlTable",
            partition_key=dynamodb.Attribute(name="shortUrl", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

        #Lambda function for URL shortening and redirecting
        Urlfunction = _lambda.Function(self, "UrlShortenerFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="aws_cdk_url_shortener.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'TABLE_NAME': table.table_name  # Pass the generated table name to the Lambda function
            }
        )

        #Grants the Lambda function read/write permissions for DYnamoDB
        table.grant_read_write_data(Urlfunction)

        #API Gateway to expose Lambda as REST API
        api = apigateway.RestApi(self, "UrlShortenerApi",
            rest_api_name="URL Shortener Service",
            description="This service shortens URLs and redirects users."
        )

        #POST/Shorten -> Lambda
        shorten_integration = apigateway.LambdaIntegration(Urlfunction)
        shorten_resource = api.root.add_resource("shorten")
        shorten_resource.add_method("POST", shorten_integration)

        #GET/{shortUrl} -> Lambda (for redirection)
        redirect_resource = api.root.add_resource("{shortUrl}")
        redirect_integration = apigateway.LambdaIntegration(Urlfunction)
        redirect_resource.add_method("GET", redirect_integration)