# Adding stack to cloudformation
    1. Go to cloudformation.
    2. Click the dropdown "Create stack".
    3. Select the "With new resources (standard)" option.
    4. Leave it on "Template is ready" under the "Prerequisite - Prepare template" section.
    5. Select "Upload a template file" under the "Specify template" section.
    6. Select "Choose file" and then select your cloudformation script.
    7. After this click "Next".
    8. Next enter your stack name and any parameters specified in your script.
    9. Click next until your script start provisioning services.

# Adding stack using CLI
  - command: aws cloudformation create-stack --stack-name test-bucket-stack-jean --template-body file://artifact_bucket_stack.yml --on-failure DELETE --parameters ParameterKey=ProjectName,ParameterValue='jean-test-project' ParameterKey=ArtifactsBucketName,ParameterValue='jean-test-bucket'

# Delete scripts using CLI
  - command: aws cloudformation delete-stack --stack-name my-stack

# Get stack status information
  - command: aws cloudformation describe-stack-events --stack-name my-stack
# Get codebuild run ids
  - command: aws codebuild list-builds-for-project --project-name project-name
# Get codebuild run details
  - command: aws codebuild batch-get-builds --ids ids
# Order in which to add scripts
    1. artifact_bucket_stack
    2. codebuild_security_stack
    3. cognito_stack
    4. code_build_stack
    5. dynamodb_stack
    
# Please note 
  - The tag seen just above the type tag for a resource and below the resource tag is the logical id of the resource
# Intrinsic Functions
    - Throughout the script you will see tags such as "!Ref" and "!Sub"
    - These are built-in functions that help you manage your stacks. Intrinsic 
      functions are used in your templates to assign values to properties that are not
      available until runtime.
    - The following intrinsic functions are used in the scripts:
            - !Ref
                - When you specify a parameter's logical name, it returns the value of the parameter.
                - When you specify a resource's logical name, it returns a value that you can 
                  typically use to refer to that resource, such as a physical ID. 
            - !Join
                - This appends a set of values into a single value, separated by 
                  the specified delimiter. If a delimiter is an empty string, the set of 
                  values are concatenated with no delimiter
            - !ImportValue
                - This returns the value of an output exported by another stack. 
                  You typically use this function to create cross-stack references.
            - !Sub
                - This substitutes variables in an input string with values that you specify. 
                  In your templates, you can use this function to construct commands or 
                  outputs that include values that aren't available until you create or update a stack.
                  For example "!Sub lambda-${AWS::Region}" will return a value such as "lambda-eu-west-1"

# Parameters
    -  Parameters enable you to input custom values to your template each time you create or update a stack.

# Outputs
    - Used to declare output values that you can import into other stacks (to create cross-stack references), 
      return in response (to describe stack calls), or view on the AWS CloudFormation console. 
      For example, you can output the S3 bucket name for a stack to make the bucket easier to find.

# Running SAM locally
  - In order to run sam locally please have the following installed:
    - Docker
    - SAM CLI
  - Use the following commands to run sam:
    - sam build
    - sam local invoke <function-logical-id>

