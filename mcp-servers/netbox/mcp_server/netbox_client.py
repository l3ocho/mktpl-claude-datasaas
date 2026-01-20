"""
NetBox API client for interacting with NetBox REST API.

Provides a generic HTTP client with methods for all standard REST operations.
Individual tool modules use this client for their specific endpoints.
"""
import requests
import logging
from typing import List, Dict, Optional, Any, Union
from urllib.parse import urljoin
from .config import NetBoxConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetBoxClient:
    """Generic client for interacting with NetBox REST API"""

    def __init__(self):
        """Initialize NetBox client with configuration"""
        config = NetBoxConfig()
        config_dict = config.load()

        self.base_url = config_dict['api_url']
        self.token = config_dict['api_token']
        self.verify_ssl = config_dict['verify_ssl']
        self.timeout = config_dict['timeout']

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.session.verify = self.verify_ssl

        logger.info(f"NetBox client initialized for {self.base_url}")

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL for API endpoint.

        Args:
            endpoint: API endpoint path (e.g., 'dcim/devices/')

        Returns:
            Full URL
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        # Ensure endpoint ends with /
        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'
        return f"{self.base_url}{endpoint}"

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response and raise appropriate errors.

        Args:
            response: requests Response object

        Returns:
            Parsed JSON response

        Raises:
            requests.HTTPError: If request failed
        """
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            # Try to get error details from response
            try:
                error_detail = response.json()
                logger.error(f"API error: {error_detail}")
            except Exception:
                logger.error(f"API error: {response.text}")
            raise e

        # Handle empty responses (e.g., DELETE)
        if response.status_code == 204 or not response.content:
            return None

        return response.json()

    def list(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        paginate: bool = True,
        limit: int = 50
    ) -> List[Dict]:
        """
        List objects from an endpoint with optional pagination.

        Args:
            endpoint: API endpoint path
            params: Query parameters for filtering
            paginate: Whether to handle pagination automatically
            limit: Number of results per page

        Returns:
            List of objects
        """
        url = self._build_url(endpoint)
        params = params or {}
        params['limit'] = limit

        logger.info(f"Listing objects from {endpoint}")

        if not paginate:
            response = self.session.get(url, params=params, timeout=self.timeout)
            result = self._handle_response(response)
            return result.get('results', []) if isinstance(result, dict) else result

        # Handle pagination
        all_results = []
        while url:
            response = self.session.get(url, params=params, timeout=self.timeout)
            result = self._handle_response(response)

            if isinstance(result, dict):
                all_results.extend(result.get('results', []))
                url = result.get('next')
                params = {}  # Next URL already contains params
            else:
                all_results.extend(result)
                break

        return all_results

    def get(self, endpoint: str, id: Union[int, str]) -> Dict:
        """
        Get a single object by ID.

        Args:
            endpoint: API endpoint path
            id: Object ID

        Returns:
            Object dictionary
        """
        url = self._build_url(f"{endpoint}/{id}")
        logger.info(f"Getting object {id} from {endpoint}")
        response = self.session.get(url, timeout=self.timeout)
        return self._handle_response(response)

    def create(self, endpoint: str, data: Dict) -> Dict:
        """
        Create a new object.

        Args:
            endpoint: API endpoint path
            data: Object data

        Returns:
            Created object dictionary
        """
        url = self._build_url(endpoint)
        logger.info(f"Creating object in {endpoint}")
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def create_bulk(self, endpoint: str, data: List[Dict]) -> List[Dict]:
        """
        Create multiple objects in bulk.

        Args:
            endpoint: API endpoint path
            data: List of object data

        Returns:
            List of created objects
        """
        url = self._build_url(endpoint)
        logger.info(f"Bulk creating {len(data)} objects in {endpoint}")
        response = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def update(self, endpoint: str, id: Union[int, str], data: Dict) -> Dict:
        """
        Update an existing object (full update).

        Args:
            endpoint: API endpoint path
            id: Object ID
            data: Updated object data

        Returns:
            Updated object dictionary
        """
        url = self._build_url(f"{endpoint}/{id}")
        logger.info(f"Updating object {id} in {endpoint}")
        response = self.session.put(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def patch(self, endpoint: str, id: Union[int, str], data: Dict) -> Dict:
        """
        Partially update an existing object.

        Args:
            endpoint: API endpoint path
            id: Object ID
            data: Fields to update

        Returns:
            Updated object dictionary
        """
        url = self._build_url(f"{endpoint}/{id}")
        logger.info(f"Patching object {id} in {endpoint}")
        response = self.session.patch(url, json=data, timeout=self.timeout)
        return self._handle_response(response)

    def delete(self, endpoint: str, id: Union[int, str]) -> None:
        """
        Delete an object.

        Args:
            endpoint: API endpoint path
            id: Object ID
        """
        url = self._build_url(f"{endpoint}/{id}")
        logger.info(f"Deleting object {id} from {endpoint}")
        response = self.session.delete(url, timeout=self.timeout)
        self._handle_response(response)

    def delete_bulk(self, endpoint: str, ids: List[Union[int, str]]) -> None:
        """
        Delete multiple objects in bulk.

        Args:
            endpoint: API endpoint path
            ids: List of object IDs
        """
        url = self._build_url(endpoint)
        data = [{'id': id} for id in ids]
        logger.info(f"Bulk deleting {len(ids)} objects from {endpoint}")
        response = self.session.delete(url, json=data, timeout=self.timeout)
        self._handle_response(response)

    def options(self, endpoint: str) -> Dict:
        """
        Get available options for an endpoint (schema info).

        Args:
            endpoint: API endpoint path

        Returns:
            Options/schema dictionary
        """
        url = self._build_url(endpoint)
        logger.info(f"Getting options for {endpoint}")
        response = self.session.options(url, timeout=self.timeout)
        return self._handle_response(response)

    def search(
        self,
        endpoint: str,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """
        Search objects using the 'q' parameter.

        Args:
            endpoint: API endpoint path
            query: Search query string
            params: Additional filter parameters

        Returns:
            List of matching objects
        """
        params = params or {}
        params['q'] = query
        return self.list(endpoint, params=params)

    def filter(
        self,
        endpoint: str,
        **filters
    ) -> List[Dict]:
        """
        Filter objects by various fields.

        Args:
            endpoint: API endpoint path
            **filters: Filter parameters (field=value)

        Returns:
            List of matching objects
        """
        return self.list(endpoint, params=filters)
