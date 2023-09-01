import json
import logging
from typing import Union
import pandas as pd
import requests
from requests.models import Response
from Notion.NotionPage import NotionPage

class NotionAPI:
    def __init__(self, notion_api_key: str):
        """Constructor for NotionAPI class.
        Checks that the key has access to the API.

        Args:
            notion_api_key (str): Notion API key used to call Notion's API
        """
        self._add_notion_api_key(notion_api_key)

    def _add_notion_api_key(self, key: str):
        """
        Internal method used by __init__.
        Sets the instance variable for the API key.
        Checks the validity of the key and tests the connection.

        Args:
            key (str): Notion API key
        """
        self.NOTION_API_KEY = key

        self._validate_key(key)
        self._validate_connection()

    def _validate_key(self, key: str):
        """
        Validates the provided API key.

        Args:
            key (str): Notion API key
        """
        if not key:
            raise ValueError("Received None as NOTION_API_KEY")
        elif not key.startswith("secret"):
            raise ValueError("Given NOTION_API_KEY does not start with 'secret'.")

    def _validate_connection(self):
        """Validates the connection to the API by making a basic query."""
        headers = self._build_headers()
        response = self._get_request("https://api.notion.com/v1/users", headers)

        if response.status_code != 200:
            raise ConnectionError(f"API connection validation failed. Status code: {response.status_code}")

    def _build_headers(self) -> dict:
        """Builds headers as expected by Notion's API."""
        headers = {
            "Notion-Version": "2021-08-16",
            "Authorization": f"Bearer {self.NOTION_API_KEY}",
        }
        return headers

    def _get_request(self, request_url: str, headers: dict) -> Response:
        """Sends a GET HTTP request to Notion's API and handles errors.
        
        Args:
            request_url (str): Request URL for the HTTP request.
            headers (dict): Headers for the HTTP request.

        Returns:
            Response: Response from the Notion API.
        """
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Received HTTP response: {response.status_code}. Reason: {response.reason}"
            )
            raise ConnectionError(e)
        
        return response

    # Additional methods for querying databases and retrieving pages can be added here



    def __init__(self, notion_api_key: str):
        """Constructor for NotionAPI class.
        Checks that the key has access to the API.

        Args:
            notion_api_key (str): Notion API key used to call Notion's API
        """
        self._add_notion_api_key(notion_api_key)

    def _add_notion_api_key(self, key: str):
        """
        Internal method used by __init__.
        Sets the instance variable for the API key.
        Checks the validity of the key and tests the connection.

        Args:
            key (str): Notion API key
        """
        self.NOTION_API_KEY = key

        self._validate_key(key)
        self._validate_connection()

    def _validate_key(self, key: str):
        """
        Validates the provided API key.

        Args:
            key (str): Notion API key
        """
        if not key:
            raise ValueError("Received None as NOTION_API_KEY")
        elif not key.startswith("secret"):
            raise ValueError("Given NOTION_API_KEY does not start with 'secret'.")

    def _validate_connection(self):
        """Validates the connection to the API by making a basic query."""
        headers = self._build_headers()
        response = self._get_request("https://api.notion.com/v1/users", headers)

        if response.status_code != 200:
            raise ConnectionError(f"API connection validation failed. Status code: {response.status_code}")

    def _build_headers(self) -> dict:
        """Builds headers as expected by Notion's API."""
        headers = {
            "Notion-Version": "2021-08-16",
            "Authorization": f"Bearer {self.NOTION_API_KEY}",
        }
        return headers

    def _get_request(self, request_url: str, headers: dict) -> Response:
        """Sends a GET HTTP request to Notion's API and handles errors.
        
        Args:
            request_url (str): Request URL for the HTTP request.
            headers (dict): Headers for the HTTP request.

        Returns:
            Response: Response from the Notion API.
        """
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Received HTTP response: {response.status_code}. Reason: {response.reason}"
            )
            raise ConnectionError(e)
        
        return response
  


    def query_db(self, db: str, query: str = "", return_type: str = "dataframe"):
        """
        Queries a database and returns the results in various possible formats.

        Args:
            db (str): Notion's db (full https link or dbid)
            query (str): Query to be sent
            return_type (str): Format for results ("dataframe", "json", "NotionPage")

        Returns:
            Union[pd.DataFrame, list[dict], list[NotionPage]]: Query results in the specified format
        """
        if db.startswith("https"):
            db = self._extract_dbid_from_http_url(db)
        # TODO: Add a check for valid dbid format if needed

        self.logger.info(f"Attempting to query database {db}")
        headers = self._build_headers()
        data = f"{query}"

        json_results = self._execute_query(db, headers, data)

        notion_pages = self._convert_to_notion_pages(json_results)

        if return_type == "json":
            return json_results
        elif return_type == "dataframe":
            return self._convert_to_dataframe(notion_pages)
        elif return_type == "NotionPage":
            return notion_pages

    def _execute_query(self, db: str, headers: dict, data: str) -> list[dict]:
        """
        Executes a database query and retrieves results.

        Args:
            db (str): Notion's db id
            headers (dict): Request headers
            data (str): Query data

        Returns:
            list[dict]: Query results as a list of dictionaries
        """
        response = self._post_request(
            f"https://api.notion.com/v1/databases/{db}/query",
            headers=headers,
            data=data,
        )
        json_content = json.loads(response.content)
        json_results = json_content["results"]

        while json_content["has_more"]:
            next_cursor = json_content["next_cursor"]
            data = {"start_cursor": next_cursor}
            response = self._post_request(
                f"https://api.notion.com/v1/databases/{db}/query",
                headers=headers,
                json_arg=data,
            )
            json_content = json.loads(response.content)
            json_results += json_content["results"]

        return json_results

    def _convert_to_notion_pages(self, json_results: list[dict]) -> list[NotionPage]:
        """
        Converts JSON query results to a list of NotionPage objects.

        Args:
            json_results (list[dict]): JSON query results

        Returns:
            list[NotionPage]: List of NotionPage objects
        """
        return [NotionPage(page) for page in json_results]
    def _convert_to_dataframe(self, notion_pages: list[NotionPage]) -> pd.DataFrame:
    
    

     def get_page(self, page_id: str) -> Response:
        """
        Queries the Notion API for a specific page and returns it.

        Args:
            page_id (str): Notion's page id (formatted or not)

        Returns:
            Response: Response from the Notion API
        """
        base_request = self._get_base_url() + "pages"

        page_id = self._format_page_id(page_id)

        request_url = f"{base_request}/{page_id}"
        headers = self._build_headers()
        response = self._get_request(request_url, headers)

        if response.status_code != 200:
            raise ValueError("Did not get response 200")

        return response

    def get_db(self, db_id: str) -> Response:
        """
        Queries the Notion API for a specific database and returns it.

        Args:
            db_id (str): Notion's db id (formatted or not)

        Returns:
            Response: Response from the Notion API
        """
        base_request = self._get_base_url() + "databases"

        db_id = self._format_page_id(db_id)

        request_url = f"{base_request}/{db_id}"
        headers = self._build_headers()
        response = self._get_request(request_url, headers)

        return response

    
    def _get_request(self, request_url: str, headers: dict) -> Response:
        """
        Sends a GET HTTP request to Notion's API and handles errors.

        Args:
            request_url (str): Request URL for the HTTP request.
            headers (dict): Headers for the HTTP request.

        Returns:
            Response: Response from the Notion API.
        """
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Received HTTP response: {response.status_code}. Reason: {response.reason}"
            )
            raise ConnectionError(e)
        
        return response
    

