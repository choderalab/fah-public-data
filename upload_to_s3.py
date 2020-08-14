import boto3
from botocore.exceptions import ClientError
from dataclasses import dataclass
import functools
import logging
from tqdm.auto import tqdm
from typing import List


@dataclass
class Upload:
    source_file: str
    dest_bucket: str
    dest_object: str


def upload_to_s3(session: boto3.Session, uploads: List[Upload]):
    s3_client = session.client("s3")

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


def _remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def get_object_key(file_name: str, strip_file_prefix: str, key_prefix: str) -> str:
    base_name = _remove_prefix(file_name, strip_file_prefix)
    key_name = base_name  # TODO change naming convention here
    return f"{key_prefix}/{key_name}"


def normalize_object_key(name: str) -> str:
    return name.replace(" ", "_")


def main(
    *files: str,
    bucket: str,
    strip_file_prefix: str,
    key_prefix: str = "",
    dry_run: bool = True,
    profile: str = "default",
):

    if normalize_object_key(key_prefix) != key_prefix:
        raise ValueError(
            f"Expected a normalized key for prefix, but got '{key_prefix}'. "
            f"Maybe '{normalize_object_key(key_prefix)}'?"
        )

    upload = (
        upload_dry_run
        if dry_run
        else functools.partial(
            upload_to_s3, boto3.session.Session(profile_name=profile)
        )
    )

    upload(
        [
            Upload(
                f,
                bucket,
                get_object_key(
                    f, strip_file_prefix=strip_file_prefix, key_prefix=key_prefix
                ),
            )
            for f in files
        ]
    )


if __name__ == "__main__":
    import fire

    fire.Fire(main)
