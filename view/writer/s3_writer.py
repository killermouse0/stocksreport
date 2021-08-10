import boto3  # type: ignore

from view.writer import Writer


class S3Writer(Writer):
    def __init__(self, bucket: str, key: str) -> None:
        self.bucket = bucket
        self.key = key
        self.s3 = boto3.client("s3")

    def write(self, data: str):
        self.s3.put_object(
            Bucket=self.bucket, Key=self.key, Body=bytearray(data, "utf-8")
        )
