AWS CDK URL Shortener
=====================

This is a simple URL shortener built with the AWS Cloud Development Kit (CDK) in Python. The project leverages **AWS Lambda**, **DynamoDB**, and **API Gateway** to create a scalable and serverless URL shortener service.

**Overview**
------------

This project demonstrates how to build a serverless URL shortener using the following AWS services:

-   **AWS Lambda**: Executes the backend logic for shortening URLs and retrieving the original URLs.
-   **Amazon DynamoDB**: A NoSQL database used to store the mapping between short URLs and their corresponding long URLs.
-   **Amazon API Gateway**: Exposes the Lambda function as an HTTPS API for interacting with the URL shortener.

**Setup and Deployment**
------------------------

### **Prerequisites**

Before setting up the project, ensure you have the following:

1.  **AWS CLI** installed and configured with your credentials. You can configure your credentials by running:

    ```bash
    aws configure
    ```

2.  **Node.js** installed. CDK requires Node.js to be installed to work properly.
3.  **AWS CDK** installed globally. If you don't have it installed yet, you can install it using:

    ```bash
    npm install -g aws-cdk
    ```

### **Project Setup**

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/aws-cdk-url-shortener.git
    cd aws-cdk-url-shortener
    ```

2.  **Install the project dependencies**: Create and activate a Python virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Linux/macOS
    .venv\Scripts\activate     # For Windows
    ```

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  **CDK Bootstrap** (if you haven't bootstrapped your AWS environment for CDK):

    ```bash
    cdk bootstrap
    ```

4.  **Synthesize the CloudFormation template**: This command will generate the CloudFormation template based on your CDK code.

    ```bash
    cdk synth
    ```

5.  **Deploy the stack**: Once the synthesis completes, deploy the stack to your AWS account:

    ```bash
    cdk deploy
    ```

    After deployment, the API Gateway endpoint will be displayed in your terminal. This will be the URL where the URL shortener service is available.

**Services Used**
-----------------

The following AWS services are used in this project:

-   **AWS Lambda**: Executes the core logic to create and retrieve short URLs.
-   **Amazon DynamoDB**: A highly scalable and managed NoSQL database used to store mappings between the short and long URLs.
-   **Amazon API Gateway**: Provides a RESTful API interface to interact with the Lambda function. It defines two routes:
    -   `POST /shorten`: Shortens a long URL.
    -   `GET /{shortUrl}`: Redirects to the long URL based on the short URL provided.

**Example Usage**
-----------------

### **1\. Shorten a URL**

To shorten a URL, make a `POST` request to the `/shorten` endpoint. The body should contain a `longUrl` field with the URL you want to shorten.

Example request:

```bash
curl -X POST -H "Content-Type: application/json"\
-d '{"longUrl":"https://example.com"}'\
https://<api-url>/prod/shorten
```

Response:

```json
{
  "shortUrl": "abc123"
}
```

This response provides a shortened URL identifier (`abc123`).

### **2\. Redirect to the Long URL**

To redirect to the original long URL, make a `GET` request using the short URL:

```bash
curl -L https://<api-url>/prod/abc123
```

This will redirect you to `https://example.com`.

**How It Works**
----------------

1.  **POST /shorten**:

    -   The API takes a long URL and generates a random 6-character short URL identifier.
    -   The mapping of `shortUrl -> longUrl` is stored in DynamoDB.
    -   The shortened URL is returned to the user.
2.  **GET /{shortUrl}**:

    -   The API takes the short URL, queries DynamoDB for the corresponding long URL, and redirects the user to that long URL.

**Testing**
-----------

Unit tests are available for the CDK stack. To run the tests:

```bash
pytest
```

The tests validate that the appropriate AWS resources (DynamoDB, Lambda, and API Gateway) are defined in the stack and that IAM policies are correctly applied.

**Cleanup**
-----------

To avoid ongoing AWS charges, you can destroy the stack when you're done with it:

```bash
cdk destroy
```

This will remove all resources created by the CDK stack.

**License**
-----------

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

* * * * *

### **Contributing**

If you'd like to contribute, feel free to submit a pull request!