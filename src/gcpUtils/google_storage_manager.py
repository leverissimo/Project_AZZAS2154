#!/usr/bin/env python
# coding: utf-8

# In[162]:


from google.oauth2 import service_account
from google.cloud import storage

class GCS_manager:
    def __init__(self, bucket_name, credential_file):
        self.bucket_name = bucket_name
        self.client = storage.Client.from_service_account_json(credential_file)
                                             
    def upload_blob(self, source_file_name, destination_blob_name, set_chunksize=None):
        """Uploads a file to the bucket.
            source_file_name = "local/path/to/file"
            destination_blob_name = "path/file"
            set_chunksize = 104857600 = 1024 * 1024 B * 100 = 100 MB Why? https://github.com/googleapis/python-storage/issues/74 
        """

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        if(set_chunksize is not None):
            blob.chunk_size = set_chunksize

        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def download_blob(self, source_blob_name, destination_file_name):
        """
            Downloads a blob from the bucket.
           source_file_name = "local/path/to/file"
            destination_blob_name = "path/file"
        """
        
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )
    
    def list_buckets(self):
        return [blob.name for blob in self.client.list_buckets()]
        
    def list_files(self, prefix =''):
        """Lists blob in the bucket."""
        if prefix == "":
            return [blob.name for blob in self.client.list_blobs(self.bucket_name)]
        else:
            return [blob.name for blob in self.client.list_blobs(self.bucket_name,prefix=prefix)]

    def make_blob_public(self, blob_name):
        """Makes a blob publicly accessible.
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"
        #
        # return public_url
        """

        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)

        blob.make_public()

        print(
            "Blob {} is publicly accessible at {}".format(
                blob.name, blob.public_url
            )
        )
        return blob.public_url