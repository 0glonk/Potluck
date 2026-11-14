# home/aws_settings_template.py

# AWS Configuration
#Keys
AWS_ACCESS_KEY_ID = "access_key_id"
AWS_SECRET_ACCESS_KEY = "secret_access_key"

#Bucket/Region
AWS_REGION = "us-east-2"
AWS_BUCKET_NAME = "potluck-app-media"
AWS_DEFAULT_ACL = "public-read"

#S3 URL
AWS_S3_CUSTOM_DOMAIN = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

#Behavior
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False