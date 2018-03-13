# django api lambda

A simple example showing how to run a django[1] app in AWS lambda using up[2].

## Deploy

```
$ up
```
 
## development
> `cat ~/.aws/credentials`
```
[apex-up-profile]
aws_access_key_id = someKeyId
aws_secret_access_key = someAccessKey
region = someAWSregion
```
> `virtualenv .venv`                             
> `source .venv/bin/activate`                            
> `pip install -r dev_requirements.txt`                                   
> `python app.py runserver 0.0.0.0:9090`                                
> `autopep8 --experimental --in-place -r -aaaaaa .`                          
> `flake8 .`                        
> to test out the app;
```
curl -X POST -H "Content-Type: application/json" \
    "http://localhost:9090/someurl"
```
 
## AWS policy
`up` requires a [policy](https://up.docs.apex.sh/#aws_credentials.iam_policy_for_up_cli) to access various resources.         
Also the user you created for the `up` profile will require policy access to dynamoDB.         
Those two policies can be combined into:         
```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:Describe*",
                "iam:CreateRole",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "cloudformation:Delete*",
                "cloudformation:Update*",
                "cloudfront:*",
                "iam:PassRole",
                "route53domains:*",
                "lambda:Create*",
                "iam:DeleteRolePolicy",
                "logs:Test*",
                "logs:FilterLogEvents",
                "cloudformation:ExecuteChangeSet",
                "sns:*",
                "iam:GetRole",
                "cloudformation:Create*",
                "lambda:InvokeFunction",
                "lambda:List*",
                "s3:*",
                "lambda:Update*",
                "lambda:Delete*",
                "iam:DeleteRole",
                "lambda:Get*",
                "cloudformation:Describe*",
                "iam:CreatePolicy",
                "logs:Put*",
                "lambda:AddPermission",
                "logs:Create*",
                "cloudwatch:*",
                "ssm:*",
                "route53:*",
                "lambda:RemovePermission",
                "acm:*",
                "dynamodb:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "apigateway:*",
            "Resource": "arn:aws:apigateway:*::/*"
        }
    ]
}
```     
Tweak that policy to be as restrictive as you want without degrading performance. It is only intended as a guide.       

Worker-function-role
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Resource": "*",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ssm:GetParametersByPath",
                "dynamodb:*"
            ]
        }
    ]
}
```                       

Also setup API gateway logging;                               
https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html                       

Postman collection: https://www.getpostman.com/collections/b97cc0bc9cd927bdd011

## Links

1. [Django](https://www.djangoproject.com/)
2. [up](https://github.com/apex/up)
