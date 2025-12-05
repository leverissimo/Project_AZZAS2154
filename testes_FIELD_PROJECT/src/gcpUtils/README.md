# GCP Utils

Biblioteca construída em python, para abstrair a utilização de serviços da GCP.


## Módulos
0. Auth
	* Retorna objeto de autenticação para outros serviços

1. Cloud Storage
	* Fazer upload de arquivos e objetos (DataFrames, etc)
	* Fazer download de arquivos
	* Fazer download de arquivos direto para objetos em Python (DataFrames, etc)
	* Listar blobs em um bucket

2. Big Query
	* Importar tabela do BQ como DataFrame
	* Exportar DataFrame como tabela do BQ

3. Vision API
	* Utilizar o serviço do Vision API (retorna request com o tipo de anotação desejada)