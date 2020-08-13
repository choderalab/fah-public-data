import boto3
from botocore.exceptions import ClientError
from dataclasses import dataclass
import logging
from tqdm.auto import tqdm
from typing import List


@dataclass
class Upload:
    source_file: str
    dest_bucket: str
    dest_object: str


def upload_to_s3(uploads: List[Upload]):
    s3_client = boto3.client("s3")
    for upload in tqdm(uploads):
        try:
            s3_client.upload_file(
                upload.source_file, upload.dest_bucket, upload.dest_object
            )
        except ClientError as e:
            logging.error(e)


def upload_dry_run(uploads: List[Upload]):
    print(
        "Dry run, showing what would be done. Use '--dry-run False' after checking this is what you want."
    )
    for upload in uploads:
        print(
            f"Would upload '{upload.source_file}' to 's3://{upload.dest_bucket}/{upload.dest_object}'"
        )


# TODO set naming convention here
def get_object_name(file_name: str) -> str:
    return file_name


def normalize_object_name(name: str) -> str:
    return name.replace(" ", "_")


def main(
    *files: str, bucket: str, prefix: str = "./", dry_run: bool = True,
):

    if normalize_object_name(prefix) != prefix:
        raise ValueError(
            f"Expected a normalized prefix, but got '{prefix}'. "
            f"Maybe '{normalize_object_name(prefix)}'?"
        )

    upload = upload_dry_run if dry_run else upload_to_s3

    upload([Upload(f, bucket, get_object_name(f)) for f in files])


if __name__ == "__main__":
    import fire

    fire.Fire(main)
