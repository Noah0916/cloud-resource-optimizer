import os
import sys
import tempfile
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from cloudopt_cli.cli import main as cli_main

def must_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"Missing env var: {name}")
    return v

def main() -> int:
    account = must_env("AZURE_STORAGE_ACCOUNT")
    in_container = must_env("INPUT_CONTAINER")
    in_blob = must_env("INPUT_BLOB")
    out_container = must_env("OUTPUT_CONTAINER")
    out_blob = must_env("OUTPUT_BLOB")

    credential = DefaultAzureCredential()
    bsc = BlobServiceClient(
        account_url=f"https://{account}.blob.core.windows.net",
        credential=credential
    )

    with tempfile.TemporaryDirectory() as td:
        in_path = os.path.join(td, "resources.csv")
        out_path = os.path.join(td, "optimization_report.csv")

        # Download input blob
        container = bsc.get_container_client(in_container)
        with open(in_path, "wb") as f:
            data = container.download_blob(in_blob).readall()
            f.write(data)

        # Run your existing CLI optimize command
        rc = cli_main(["optimize", "--input", in_path, "--output", out_path])
        if rc != 0:
            return rc

        # Upload output blob
        outc = bsc.get_container_client(out_container)
        with open(out_path, "rb") as f:
            outc.upload_blob(name=out_blob, data=f, overwrite=True)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
