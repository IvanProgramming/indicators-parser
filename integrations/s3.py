import boto3 as boto3

from settings import REPORTS_FOLDER, ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, REGION_NAME, BUCKET_NAME

s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT_URL,
    region_name=REGION_NAME,
)


def save_report_to_s3(file, report_id, is_public=False):
    """
        Saves the report to S3

        Args:
            file: Report file
            report_id: Report ID
            is_public: Flag, shows, might this report and all indicators from it become public
    """
    file_path = f"{REPORTS_FOLDER}/{report_id}.pdf"
    s3_client.upload_file(file, BUCKET_NAME, file_path)

    if is_public:
        s3_client.put_object_acl(ACL="public-read", Bucket=BUCKET_NAME, Key=file_path)

    return file_path


def remove_report_from_s3(report_id):
    """
        Removes the report from S3

        Args:
            report_id: Report ID
    """
    file_path = f"{REPORTS_FOLDER}/{report_id}.pdf"
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_path)

    return file_path


def generate_report_url(report_id):
    """
        Generates the report URL

        Args:
            report_id: Report ID
    """
    file_path = f"{REPORTS_FOLDER}/{report_id}.pdf"
    url = s3_client.generate_presigned_url("get_object", Params={
        "Bucket": BUCKET_NAME,
        "Key": file_path,
    }, ExpiresIn=3600 * 24)

    return url
