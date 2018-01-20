
# ussd lambda

A simple example showing how to run a ussd app (or any django[1] app really) in AWS lambda using up[2].

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
> `virtualenv -p python3 .venv`                             
> `source .venv/bin/activate`                            
> `pip3 install -r dev_requirements.txt`                                   
> `python3 app.py runserver 0.0.0.0:9090`                  
> `autopep8 --experimental --in-place -r -aaaaaa .`                          
> `flake8 .`                        
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"phonessionId": "10p5","text":"1", "serviceCode": "312"}' \
    "http://localhost:$PORT/ussd"
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

Postman collection: https://www.getpostman.com/collections/b97cc0bc9cd927bdd011

## Links

1. [Django](https://www.djangoproject.com/)
2. [up](https://github.com/apex/up)
