from google.cloud import storage
from .osUtils import *

#=================================BLOB MODULES=================================#

def getBlob(projectName: str,
             bucketFullPath: str,
             credentials):

    """
    Get a blob from GCS


    :param projectName: project name in GCP
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param credentials: Google OAuth2 service account credentials object
    """

    client = storage.Client(projectName, credentials)
    bucket = client.get_bucket(bucketFullPath.split('/')[0]) #Gets bucket
    blob = bucket.blob(bucketFullPath.split('/',1)[1])

    return blob

def listBlobs(projectName,
			  bucketName,
			  credentials):

	client = storage.Client(projectName, credentials)
	

	return [blob for blob in storage_client.list_blobs(bucket_name)]

#=================================UPLOAD MODULES=================================#


def fileUploadToStorage(projectName: str,
						 bucketFullPath: str,
						 objPath: str,
                         credentials):
    
    """
    Uploads a file to GCS


    :param projectName: project name in GCP
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param objPath: path to object to upload
    :param credentials: Google OAuth2 service account credentials object
	"""

    
    blob = getBlob(projectName, bucketFullPath, credentials)
    blob.upload_from_filename(objPath)
    
    print('File uploaded')

def objUploadToStorage(projectName: str, 
						bucketFullPath: str, 
						objectToUpload,
                        fileType:str,
                        credentials): 
    
    """
    Uploads a object to GCS


    :param projectName: project name in GCP
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param objectToUpload: csv, parquet or json to upload
    :param fileType: 'text/csv' | 'application/octet-stream' | 'application/json'
    :param credentials: Google OAuth2 service account credentials object
	"""
    
    blob = getBlob(projectName, bucketFullPath, credentials) 

    blob.upload_from_string(objectToUpload, fileType)
    
    print('Object uploaded')


def uploadAllFilesToStorage(folderPath: str, 
							projectName: str, 
							bucketFullPath: str,
                            credentials):
    
    """
    Uploads all images from folder to GCS 

    :param projectName: project name in google cloud 
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param folderPath: path to image to upload 
    :param credentials: Google OAuth2 service account credentials object
    """
    import time

    t = time.process_time() #Variable to track time
    imgs = getFilesFull(folderPath)
    
    print('--Initiating --')
    print(f'Total files: {len(imgs)}')
    
    errors = {}
    track = 0
    for each in imgs:

        track += 1
        
        eachName = each.split('\\')[-1:][0].split('.')[0]


        t1 = time.process_time()
        print('-'*20)
        print(f'processing object: {eachName}')
        print(f'Object: {track}')

        try:

            fileUploadToStorage(projectName, bucketFullPath, each, credentials)

        except Exception as e:

            print(e)
            errors[eachName] = e

        elapsed_time1 = time.process_time() - t1
        print(f'Elapsed time: {elapsed_time1} seconds.')


    print(f'Total errors: {len(errors)}')
    elapsed_time = time.process_time() - t
    print(f'--Total elapsed time: {elapsed_time} seconds--')

    print('Files uploaded')


#=================================DOWNLOAD MODULES=================================#


def objDonwloadFromStorage(projectName: str, 
                            bucketFullPath: str,
                            credentials):

    """
    Donwloads file from GSC

    :param projectName: project name in GCP
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param obj: object to download
    :param credentials: Google OAuth2 service account credentials object
    """
    from io import BytesIO

    blob = getBlob(projectName, bucketFullPath, credentials)

    byte_stream = BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)

    return byte_stream


def fileDonwloadFromStorage(projectName: str, 
                            bucketFullPath: str,
                            fileSavePath:str,
                            credentials):

    """
    Donwloads file from GSC

    :param projectName: project name in GCP
    :param bucketFullPath: <bucketName>/<folders>/.../<object>
    :param fileSavePath: your local path to save file
    :param credentials: Google OAuth2 service account credentials object
    """

    blob = getBlob(projectName, bucketFullPath, credentials) 

    blob.download_to_filename(fileSavePath)    

    print('File downloaded')
 