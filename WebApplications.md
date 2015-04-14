Go to the source directory you downloaded and run Weather/interface.py which starts a WSGI server that handles various applications. Applications include

  * **detail** - station detail view
  * **list** - list of all stations
  * **zip** - lookup by zipcode
  * **location** - lookup by location
  * **update** - update observation base


Just point your browser to http://localhost:8000/ `<app_name>` and have at it. The parameters are QUERY\_STRING driven so stuff like http://localhost:8000/zip?21202 or http://localhost:8000/location?baltimore,md will work just fine