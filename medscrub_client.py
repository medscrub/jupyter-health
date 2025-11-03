"""
MedScrub Python Client
A simple Python wrapper for the MedScrub FHIR de-identification API

Usage:
    from medscrub_client import MedScrubClient

    client = MedScrubClient(jwt_token="your-jwt-token")

    # De-identify a FHIR Patient resource
    result = client.deidentify_fhir(patient_resource)
    print(f"Session ID: {result['sessionId']}")

    # Re-identify using the session ID
    original = client.reidentify_fhir(result['deidentifiedResource'], result['sessionId'])
"""

import requests
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class MedScrubConfig:
    """Configuration for MedScrub API client"""
    api_url: str = "https://api.medscrub.dev"
    jwt_token: Optional[str] = None
    api_key: Optional[str] = None
    timeout: int = 30


class MedScrubError(Exception):
    """Base exception for MedScrub API errors"""
    pass


class MedScrubAuthError(MedScrubError):
    """Authentication error (401)"""
    pass


class MedScrubRateLimitError(MedScrubError):
    """Rate limit exceeded (429)"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class MedScrubClient:
    """
    Client for interacting with MedScrub FHIR de-identification API

    Attributes:
        config: Configuration object with API URL and credentials
    """

    def __init__(
        self,
        jwt_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: str = "https://api.medscrub.dev"
    ):
        """
        Initialize MedScrub client

        Args:
            jwt_token: JWT token from medscrub.dev/playground
            api_key: Alternative API key (for local deployment)
            api_url: API base URL (default: https://api.medscrub.dev)
        """
        self.config = MedScrubConfig(
            api_url=api_url,
            jwt_token=jwt_token,
            api_key=api_key
        )

        if not jwt_token and not api_key:
            raise ValueError("Either jwt_token or api_key must be provided")

    def _get_headers(self) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MedScrub-Python-Client/1.0"
        }

        if self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"
        elif self.config.api_key:
            headers["X-API-Key"] = self.config.api_key

        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        if response.status_code == 401:
            raise MedScrubAuthError(
                f"Authentication failed: {response.json().get('message', 'Invalid credentials')}"
            )

        if response.status_code == 429:
            retry_after = response.headers.get('X-RateLimit-Reset')
            raise MedScrubRateLimitError(
                "Rate limit exceeded. Please wait before retrying.",
                retry_after=int(retry_after) if retry_after else None
            )

        if response.status_code >= 400:
            error_data = response.json() if response.content else {}
            raise MedScrubError(
                f"API error ({response.status_code}): {error_data.get('message', 'Unknown error')}"
            )

        return response.json()

    def deidentify_fhir(
        self,
        resource: Dict[str, Any],
        session_id: Optional[str] = None,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        De-identify a FHIR resource or Bundle

        Args:
            resource: FHIR resource (Patient, Observation, etc.) or Bundle
            session_id: Optional session ID for continued de-identification
            output_format: Output format - "json" (default), "json-compact", "python-dict", or "llm-optimized"

        Returns:
            Dictionary containing:
                - deidentifiedResource: De-identified FHIR resource (format depends on output_format)
                - sessionId: Session ID for re-identification
                - detectedPHI: List of detected PHI fields
                - processingTime: Processing time in milliseconds

        Example:
            patient = {
                "resourceType": "Patient",
                "id": "example-patient",
                "name": [{"family": "Smith", "given": ["John"]}],
                "birthDate": "1990-01-15"
            }

            # Standard JSON format
            result = client.deidentify_fhir(patient)
            print(f"De-identified: {result['deidentifiedResource']}")
            print(f"Session ID: {result['sessionId']}")

            # Python dict format (for Jupyter notebooks)
            result = client.deidentify_fhir(patient, output_format="python-dict")
            print(result['deidentifiedResource'])  # Copy/paste ready Python dict
        """
        url = f"{self.config.api_url}/api/fhir/deidentify"

        payload = {
            "resource": resource,
            "outputFormat": output_format
        }
        if session_id:
            payload["sessionId"] = session_id

        response = requests.post(
            url,
            headers=self._get_headers(),
            json=payload,
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def reidentify_fhir(
        self,
        resource: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Re-identify a de-identified FHIR resource

        Args:
            resource: De-identified FHIR resource
            session_id: Session ID from de-identification

        Returns:
            Dictionary containing:
                - reidentifiedResource: Original FHIR resource restored
                - sessionId: Session ID used
                - processingTime: Processing time in milliseconds

        Example:
            original = client.reidentify_fhir(
                deidentified_resource,
                session_id="abc123"
            )
            print(f"Original: {original['reidentifiedResource']}")
        """
        url = f"{self.config.api_url}/api/fhir/reidentify"

        response = requests.post(
            url,
            headers=self._get_headers(),
            json={
                "resource": resource,
                "sessionId": session_id
            },
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """
        Get information about a de-identification session

        Args:
            session_id: Session ID to query

        Returns:
            Dictionary with session details:
                - sessionId: Session ID
                - tokenCount: Number of PHI tokens stored
                - createdAt: Session creation time
                - expiresAt: Session expiration time
                - hoursRemaining: Hours until expiration
        """
        url = f"{self.config.api_url}/api/session"

        response = requests.get(
            url,
            headers=self._get_headers(),
            params={"sessionId": session_id},
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Delete a de-identification session and its PHI mappings

        Args:
            session_id: Session ID to delete

        Returns:
            Dictionary with deletion confirmation
        """
        url = f"{self.config.api_url}/api/session"

        response = requests.delete(
            url,
            headers=self._get_headers(),
            params={"sessionId": session_id},
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def deidentify_text(
        self,
        text: str,
        session_id: Optional[str] = None,
        confidence_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        De-identify unstructured text

        Args:
            text: Clinical text to de-identify
            session_id: Optional session ID for continued de-identification
            confidence_threshold: Minimum confidence for entity detection (0-1)

        Returns:
            Dictionary containing:
                - deidentifiedText: De-identified text
                - sessionId: Session ID for re-identification
                - detectedEntities: List of detected PHI entities
                - processingTime: Processing time in milliseconds
        """
        url = f"{self.config.api_url}/api/deidentify"

        payload = {
            "text": text,
            "options": {"confidenceThreshold": confidence_threshold}
        }
        if session_id:
            payload["sessionId"] = session_id

        response = requests.post(
            url,
            headers=self._get_headers(),
            json=payload,
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def reidentify_text(
        self,
        text: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Re-identify de-identified text

        Args:
            text: De-identified text
            session_id: Session ID from de-identification

        Returns:
            Dictionary containing:
                - reidentifiedText: Original text restored
                - sessionId: Session ID used
                - processingTime: Processing time in milliseconds
        """
        url = f"{self.config.api_url}/api/reidentify"

        response = requests.post(
            url,
            headers=self._get_headers(),
            json={
                "text": text,
                "sessionId": session_id
            },
            timeout=self.config.timeout
        )

        return self._handle_response(response)

    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status

        Returns:
            Dictionary with health status
        """
        url = f"{self.config.api_url}/health"

        response = requests.get(url, timeout=self.config.timeout)
        return self._handle_response(response)


# Example usage
if __name__ == "__main__":
    # Initialize client (get JWT token from https://medscrub.dev/playground)
    client = MedScrubClient(jwt_token="your-jwt-token-here")

    # Example FHIR Patient resource
    patient = {
        "resourceType": "Patient",
        "id": "example-patient-001",
        "name": [
            {
                "family": "Smith",
                "given": ["John", "Robert"],
                "text": "John Robert Smith"
            }
        ],
        "birthDate": "1990-01-15",
        "gender": "male",
        "telecom": [
            {
                "system": "email",
                "value": "john.smith@example.com"
            }
        ]
    }

    try:
        # De-identify the patient resource
        print("De-identifying FHIR Patient resource...")
        result = client.deidentify_fhir(patient)

        print(f"\n✓ De-identification successful!")
        print(f"Session ID: {result['sessionId']}")
        print(f"PHI fields detected: {len(result.get('detectedPHI', []))}")
        print(f"Processing time: {result.get('processingTime', 0)}ms")

        # Print de-identified resource
        print("\nDe-identified Patient:")
        print(json.dumps(result['deidentifiedResource'], indent=2))

        # Re-identify the resource
        print("\n\nRe-identifying resource...")
        original = client.reidentify_fhir(
            result['deidentifiedResource'],
            result['sessionId']
        )

        print("\n✓ Re-identification successful!")
        print("Original Patient:")
        print(json.dumps(original['reidentifiedResource'], indent=2))

        # Get session info
        print("\n\nSession Information:")
        session_info = client.get_session_info(result['sessionId'])
        print(json.dumps(session_info, indent=2))

        # Clean up: delete session
        print("\n\nDeleting session...")
        client.delete_session(result['sessionId'])
        print("✓ Session deleted")

    except MedScrubAuthError as e:
        print(f"❌ Authentication error: {e}")
        print("Get a JWT token from https://medscrub.dev/playground")
    except MedScrubRateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        if e.retry_after:
            print(f"Retry after: {e.retry_after} seconds")
    except MedScrubError as e:
        print(f"❌ API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
