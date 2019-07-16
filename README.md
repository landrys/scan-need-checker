# scan-need-checker

- serverless create --template aws-python3  --name scan-need-checker  --path scan-need-checker
- virtualenv venv --python=python3
- source venv/bin/activate
- Add dep in requirements.txt file and have Docker running.

- to deploy
  - serverless deploy
  - serverless invoke -f scan-checker --log
- to remove
  - serverless remove
- to run locally look at data.json and .ch for serverless command
