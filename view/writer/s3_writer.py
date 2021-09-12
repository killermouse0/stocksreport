from typing import Dict

import boto3  # type: ignore

from view.writer import Writer


class S3Writer(Writer):
    def __init__(self, bucket: str, prefix: str) -> None:
        self.bucket = bucket
        self.prefix = prefix
        self.s3 = boto3.client("s3")

    def write(self, data_by_id: Dict[str, str]):
        for (id, data) in data_by_id.items():
            key = f"{self.prefix}/{id}.js"
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                ContentType="text/javascript",
                Body=bytearray(data, "utf-8"),
            )
