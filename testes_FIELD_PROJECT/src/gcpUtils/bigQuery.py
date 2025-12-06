from google.cloud import bigquery

#=================================GET TABLE PANDAS=================================#

def tableToPandas(query: str,
				project: str,
				credentials):
		
	"""
    Gets a BQ table to pandas DF

	:param query: BQ native query
    :param project: BQ project name (not equal GCP project) 
    :param credentials: Google OAuth2 service account credentials object
	"""

	return bigquery.Client(project, credentials).query(query).to_dataframe()


def pandasToBq(df,
				project: str,
				tableId: str,
				truncate: bool,
				credentials):

	
	"""
    Gets a BQ table to pandas DF

	:param df: pandas DF to upload
    :param project: BQ project name (not equal GCP project) 
    :param tableId: dataset.tablename
    :param credentials: Google OAuth2 service account credentials object
	"""
	client = bigquery.Client(project, credentials)

	if truncate:
		client.delete_table(tableId, not_found_ok=True)

	job = client.load_table_from_dataframe(df, tableId)

	return job.result()
