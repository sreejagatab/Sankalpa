import os
import requests
from typing import Dict, Any, List, Optional, Union
import base64
import json

from sankalpa.core import get_logger
from sankalpa.core.caching import cache

logger = get_logger("integrations.github")

class GitHubClient:
    """GitHub API client for Sankalpa integrations"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client
        
        Args:
            token: GitHub personal access token
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            logger.warning("GitHub token not found. Some functionality will be limited.")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a request to the GitHub API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            headers: Additional headers
            
        Returns:
            Response data
            
        Raises:
            Exception: If the request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Set up headers
        request_headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        if self.token:
            request_headers["Authorization"] = f"token {self.token}"
            
        if headers:
            request_headers.update(headers)
            
        # Make the request
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers
            )
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {}
                
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {str(e)}")
            
            if hasattr(e, 'response') and e.response is not None:
                error_data = e.response.json() if e.response.content else {}
                logger.error(f"GitHub API error: {error_data}")
                raise Exception(f"GitHub API error: {error_data.get('message', str(e))}")
            else:
                raise Exception(f"GitHub API request failed: {str(e)}")
    
    def get_user(self) -> Dict[str, Any]:
        """Get authenticated user information
        
        Returns:
            User information
        """
        return self._make_request("GET", "/user")
    
    def list_repositories(
        self, 
        username: Optional[str] = None,
        org: Optional[str] = None,
        sort: str = "updated",
        direction: str = "desc",
        per_page: int = 30,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """List repositories
        
        Args:
            username: Username to list repositories for
            org: Organization to list repositories for
            sort: Sort field (created, updated, pushed, full_name)
            direction: Sort direction (asc, desc)
            per_page: Number of results per page
            page: Page number
            
        Returns:
            List of repositories
        """
        if username:
            endpoint = f"/users/{username}/repos"
        elif org:
            endpoint = f"/orgs/{org}/repos"
        else:
            endpoint = "/user/repos"
            
        params = {
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository information
        """
        endpoint = f"/repos/{owner}/{repo}"
        return self._make_request("GET", endpoint)
    
    def create_repository(
        self,
        name: str,
        description: Optional[str] = None,
        private: bool = False,
        auto_init: bool = False,
        org: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether the repository is private
            auto_init: Whether to initialize with a README
            org: Organization to create the repository in
            
        Returns:
            Repository information
        """
        data = {
            "name": name,
            "private": private,
            "auto_init": auto_init
        }
        
        if description:
            data["description"] = description
            
        if org:
            endpoint = f"/orgs/{org}/repos"
        else:
            endpoint = "/user/repos"
            
        return self._make_request("POST", endpoint, data=data)
    
    def get_file_contents(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get file contents from a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            ref: Git reference (branch, tag, or commit)
            
        Returns:
            File information and contents
        """
        endpoint = f"/repos/{owner}/{repo}/contents/{path}"
        params = {}
        
        if ref:
            params["ref"] = ref
            
        response = self._make_request("GET", endpoint, params=params)
        
        # Decode content if it exists
        if "content" in response and response["encoding"] == "base64":
            content = base64.b64decode(response["content"]).decode("utf-8")
            response["decoded_content"] = content
            
        return response
    
    def create_or_update_file(
        self,
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: Optional[str] = None,
        sha: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create or update a file in a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            content: File content
            message: Commit message
            branch: Branch name
            sha: SHA of the file to update (required for updates)
            
        Returns:
            Commit information
        """
        endpoint = f"/repos/{owner}/{repo}/contents/{path}"
        
        # Encode content as base64
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        data = {
            "message": message,
            "content": encoded_content
        }
        
        if branch:
            data["branch"] = branch
            
        if sha:
            data["sha"] = sha
            
        return self._make_request("PUT", endpoint, data=data)
    
    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
        draft: bool = False
    ) -> Dict[str, Any]:
        """Create a pull request
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Pull request title
            head: Head branch
            base: Base branch
            body: Pull request description
            draft: Whether the PR is a draft
            
        Returns:
            Pull request information
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        
        data = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft
        }
        
        if body:
            data["body"] = body
            
        return self._make_request("POST", endpoint, data=data)
    
    def list_pull_requests(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        sort: str = "created",
        direction: str = "desc",
        per_page: int = 30,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """List pull requests
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: PR state (open, closed, all)
            sort: Sort field (created, updated, popularity, long-running)
            direction: Sort direction (asc, desc)
            per_page: Number of results per page
            page: Page number
            
        Returns:
            List of pull requests
        """
        endpoint = f"/repos/{owner}/{repo}/pulls"
        
        params = {
            "state": state,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        return self._make_request("GET", endpoint, params=params)
    
    def list_workflows(
        self,
        owner: str,
        repo: str,
        per_page: int = 30,
        page: int = 1
    ) -> Dict[str, Any]:
        """List GitHub Actions workflows
        
        Args:
            owner: Repository owner
            repo: Repository name
            per_page: Number of results per page
            page: Page number
            
        Returns:
            List of workflows
        """
        endpoint = f"/repos/{owner}/{repo}/actions/workflows"
        
        params = {
            "per_page": per_page,
            "page": page
        }
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_workflow_runs(
        self,
        owner: str,
        repo: str,
        workflow_id: Union[int, str],
        branch: Optional[str] = None,
        status: Optional[str] = None,
        per_page: int = 30,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get workflow runs
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID or file name
            branch: Branch to filter by
            status: Status to filter by
            per_page: Number of results per page
            page: Page number
            
        Returns:
            List of workflow runs
        """
        endpoint = f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
        
        params = {
            "per_page": per_page,
            "page": page
        }
        
        if branch:
            params["branch"] = branch
            
        if status:
            params["status"] = status
            
        return self._make_request("GET", endpoint, params=params)
    
    def dispatch_workflow(
        self,
        owner: str,
        repo: str,
        workflow_id: Union[int, str],
        ref: str,
        inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Trigger a workflow run
        
        Args:
            owner: Repository owner
            repo: Repository name
            workflow_id: Workflow ID or file name
            ref: Git reference (branch, tag)
            inputs: Workflow inputs
            
        Returns:
            Empty dict on success
        """
        endpoint = f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
        
        data = {
            "ref": ref
        }
        
        if inputs:
            data["inputs"] = inputs
            
        return self._make_request("POST", endpoint, data=data)
    
    def create_github_app_token(
        self,
        app_id: str,
        private_key: str,
        installation_id: str
    ) -> str:
        """Create a GitHub App installation token
        
        Args:
            app_id: GitHub App ID
            private_key: GitHub App private key
            installation_id: Installation ID
            
        Returns:
            Installation token
        """
        # This is just a stub - implementing JWT creation and token exchange
        # requires additional libraries and is beyond the scope of this example
        raise NotImplementedError("GitHub App token creation not implemented")

# Create a default client
github_client = GitHubClient()