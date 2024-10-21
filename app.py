#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk_url_shortener.aws_cdk_url_shortener_stack import AwsCdkUrlShortenerStack


app = cdk.App()
AwsCdkUrlShortenerStack(app, "AwsCdkUrlShortenerStack",)

app.synth()
