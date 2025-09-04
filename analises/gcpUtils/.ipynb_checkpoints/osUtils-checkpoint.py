import os

def getFilesFull(folderPath:str) -> list:
    """
    Retrieve a full path for all objects in a directory (c://full/path/object)

    :param folderPath: path to directory to return the files 
	"""

    return [os.path.join(folderPath, each) for each in os.listdir(folderPath)]

def getFilesNames(folderPath:str) -> list:
    """
    Retrieve names for all objects in a directory (object.csv)

    :param folderPath: path to directory to return the files
	"""

    return [each for each in os.listdir(folderPath)]

def createDir(dirPath:str, 
				folderName:str):
    """
	Creates a directory if not exists

	:param dirPath: directory for creating the folder
	:param folderName: folder name
    """
    try:
        os.mkdir(os.path.join(dirPath,folderName))
        
        print('Dir created')
        
    
    except:
        print('Dir already created')
