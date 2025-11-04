"""
⚠️ VULNERABLE CODE - FOR LIVE DEMO ONLY ⚠️

This file demonstrates creating a public Google Cloud Storage (GCS) bucket,
which is a common security misconfiguration.

USE THIS DURING THE LIVE DEMO to show:
1. Snyk IaC detecting public GCS buckets from Terraform code.
2. Snyk Code detecting insecure bucket configurations in Python code.

DO NOT USE IN PRODUCTION!
"""

from google.cloud import storage

def create_public_gcs_bucket(bucket_name):
    """
    Creates a new GCS bucket and makes it publicly accessible.
    This is a significant security risk.
    """
    storage_client = storage.Client()

    # 🔴 VULNERABLE: Creating a bucket without enforcing uniform bucket-level access
    # This allows for fine-grained ACLs, which can easily lead to misconfigurations.
    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created.")

    # 🔴 VULNERABLE: Making the bucket public
    # This gives anyone on the internet read access to all objects in the bucket.
    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": {"allUsers"}}
    )
    bucket.set_iam_policy(policy)

    print(f"Bucket {bucket.name} is now publicly readable.")
    print("This is a security vulnerability!")

    return bucket

if __name__ == '__main__':
    # This is for demonstration purposes. In a real application,
    # the bucket name should not be hardcoded.
    # Replace 'your-unique-bucket-name' with a globally unique bucket name.
    # For the demo, we can use a placeholder.
    demo_bucket_name = "gemini-demo-public-bucket-12345"
    print("⚠️  WARNING: This script creates a public GCS bucket.")
    print("    This is a security risk and should not be done in production.")
    try:
        create_public_gcs_bucket(demo_bucket_name)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("This might be due to permissions or the bucket name already existing.")
