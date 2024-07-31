import requests  # Assuming 'requests' library is installed
import urllib3

class FortiAnalyzer:
    """
    This class represents a Fortinet Analyzer instance and provides methods
    for logging in, generating reports, checking report status, downloading
    reports, and deleting reports.
    """

    def __init__(self, host, base_url="https://{host}/jsonrpc", adom="root"):
        """
        Initializes the FortiAnalyzer object.

        Args:
            host (str): The IP address or hostname of the FortiAnalyzer instance.
            base_url (str, optional): The base URL for the Fortinet API. Defaults to "https://{host}/jsonrpc".
            adom (str): The administrative domain. Defaults to "root".
        """

        self.host = host
        self.session_key = None
        self.base_url = base_url.format(host=self.host)
        self.adom = adom
        urllib3.disable_warnings()

    def send_request(self, method, params, use_session_key=True, verify=False):
        """
        Sends an HTTP request to the Fortinet Analyzer API.

        Args:
            method (str): The JSONRPC method (e.g., exec, get, add, delete).
            params (dict): A dictionary of query parameters.

        Returns:
            requests.Response: The response object from the HTTP request.
        """

        data = {
            "id": "1",
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }

        if (use_session_key):
            data["session"] = self.session_key

        response = requests.request("POST", url=self.base_url, json=data, verify=verify)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response

    def login(self, username, password):
        """
        Logs in to the FortiAnalyzer instance.

        Args:
            username (str): The username for the FortiAnalyzer account.
            password (str): The password for the FortiAnalyzer account.

        Returns:
            bool: True if login is successful, False otherwise.
        """

        params = [{
            "url": "/sys/login/user",
            "data": {
                "user": username,
                "passwd": password
            }
        }]
        response = self.send_request("exec", params=params, use_session_key=False)

        if response.status_code == 200:
            response_obj = response.json()
            if not response_obj.get("result"):
                print("Error: invalid response")
                return False
            if not response_obj["result"][0]["status"]["code"] == 0:
                err_code = response_obj["result"][0]["status"]["code"]
                err_message = response_obj["result"][0]["status"]["message"]
                print(f"Error {err_code}: {err_message}")
            self.session_key = response_obj["session"]
            return True
        else:
            return False

    def generate_report(self, device, layout_id, time_period="today"):
        """
        Generates a report on the FortiAnalyzer device.

        Args:
            device (str): The device name.
            layout_id (int): The ID of the report layout to generate.
            time_period (str): The type of time period. Defaults to "today".

        Returns:
            str: The task ID of the generated report, or None if generation fails.
        """

        if self.session_key is None:
            print("Error: Not logged in. Please login first.")
            return None

        params = [{
            "apiver": 3,
            "url": f"/report/adom/{self.adom}/run",
            "schedule": "1",
            "schedule-param": {
                "device": device,
                "layout-id": layout_id,
                "time-period": time_period
            }
        }]
        response = self.send_request("add", params=params)
        if response.status_code == 200:
            response_obj = response.json()
            if response_obj.get("error"):
                err_code = response_obj["error"]["code"]
                err_message = response_obj["error"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            if not response_obj.get("result"):
                print("Error: invalid response")
                return None
            if (
                response_obj["result"].get("status") and
                response_obj["result"]["status"].get("code") and
                response_obj["result"]["status"]["code"] != 0
            ):
                err_code = response_obj["result"]["status"]["code"]
                err_message = response_obj["result"]["status"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            return response_obj["result"]["tid"]
        else:
            return None

    def get_report_state(self, task_id):
        """
        Gets the progress of a report generation task.

        Args:
            task_id (str): The ID of the report generation task.

        Returns:
            int: The percentage completion of the report generation task (0-100),
                or None if task ID is invalid or report state cannot be retrieved.
        """

        if self.session_key is None:
            print("Error: Not logged in. Please login first.")
            return None

        params = [{
            "apiver": 3,
            "url": f"/report/adom/{self.adom}/run/{task_id}",
        }]
        response = self.send_request("get", params=params)
        if response.status_code == 200:
            response_obj = response.json()
            if response_obj.get("error"):
                err_code = response_obj["error"]["code"]
                err_message = response_obj["error"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            if not response_obj.get("result"):
                print("Error: invalid response")
                return None
            if (
                response_obj["result"].get("status") and
                response_obj["result"]["status"].get("code") and
                response_obj["result"]["status"]["code"] != 0
            ):
                err_code = response_obj["result"]["status"]["code"]
                err_message = response_obj["result"]["status"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            return response_obj["result"]["progress-percent"]
        else:
            return None

    def download_report(self, task_id):
        """
        Downloads a generated report.

        Args:
            task_id (str): The ID of the generated report.

        Returns:
            str: The report data in XML format, or None if download fails.
        """

        if self.session_key is None:
            print("Error: Not logged in. Please login first.")
            return None

        params = [{
            "apiver": 3,
            "data-type": "text",
            "format": "xml",
            "url": f"/report/adom/{self.adom}/reports/data/{task_id}",
        }]
        response = self.send_request("get", params=params)
        if response.status_code == 200:
            response_obj = response.json()
            if response_obj.get("error"):
                err_code = response_obj["error"]["code"]
                err_message = response_obj["error"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            if not response_obj.get("result"):
                print("Error: invalid response")
                return None
            if (
                response_obj["result"].get("status") and
                response_obj["result"]["status"].get("code") and
                response_obj["result"]["status"]["code"] != 0
            ):
                err_code = response_obj["result"]["status"]["code"]
                err_message = response_obj["result"]["status"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            return response_obj["result"]["data"]
        else:
            return None
    
    def delete_report(self, task_id):
        """
        Deletes a generated report.

        Args:
            task_id (str): The ID of the generated report.

        Returns:
            bool: True if deletion is successful, False otherwise.
        """

        if self.session_key is None:
            print("Error: Not logged in. Please login first.")
            return None

        params = [{
            "apiver": 3,
            "url": f"/report/adom/{self.adom}/reports/data/{task_id}",
        }]
        response = self.send_request("delete", params=params)
        if response.status_code == 200:
            response_obj = response.json()
            if response_obj.get("error"):
                err_code = response_obj["error"]["code"]
                err_message = response_obj["error"]["message"]
                print(f"Error {err_code}: {err_message}")
                return None
            if not response_obj.get("result"):
                print("Error: invalid response")
                return False
            if (
                response_obj["result"].get("status") and
                response_obj["result"]["status"].get("code") and
                response_obj["result"]["status"]["code"] != 0
            ):
                err_code = response_obj["result"]["status"]["code"]
                err_message = response_obj["result"]["status"]["message"]
                print(f"Error {err_code}: {err_message}")
                return False
            return True
        else:
            return False
