from google.cloud import vision



def getImageFeatures(imgPath:str,
					 features:list
					 credentials):

	
	    """
    Get a blob from GCS


    :param imgPath: image path
    :param features: feature type (numbers)
    	CROP_HINTS = 9
		DOCUMENT_TEXT_DETECTION = 11
		FACE_DETECTION = 1
		IMAGE_PROPERTIES = 7
		LABEL_DETECTION = 4
		LANDMARK_DETECTION = 2
		LOGO_DETECTION = 3
		OBJECT_LOCALIZATION = 19
		PRODUCT_SEARCH = 12
		SAFE_SEARCH_DETECTION = 6
		TEXT_DETECTION = 5
		TYPE_UNSPECIFIED = 0
		WEB_DETECTION = 10
    :param credentials: Google OAuth2 service account credentials object
    """

    client = vision.ImageAnnotatorClient(credentials)
    
    #Loads image
    with io.open(imgPath, 'rb') as image_file:
        content = image_file.read()
    
    #Instanciates Image
    targetImage = vision.Image(content=content)
    
    #Gets labels and properties
    response = client.annotate_image({
        'image': targetImage,
        'features': [{'type_': each, 'max_results':10000} for each in features]
    })

    return response