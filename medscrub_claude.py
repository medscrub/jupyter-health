"""
MedScrub + Claude API Integration
Safe healthcare AI workflows with automatic PHI de-identification

This module enables direct Claude API calls from Jupyter notebooks with
automatic PHI scrubbing and re-identification - no copy/paste needed!

Usage:
    from medscrub_claude import MedScrubClaude

    client = MedScrubClaude(
        medscrub_jwt="your-medscrub-jwt",
        claude_api_key="your-claude-api-key"
    )

    # Ask Claude about patient data - PHI automatically scrubbed!
    response = client.ask_about_fhir(
        resource=patient_data,
        question="What medications is this patient taking?"
    )

    print(response['answer'])  # Claude's response with original PHI restored
"""

import anthropic
from typing import Dict, Any, Optional, List
from medscrub_client import MedScrubClient, MedScrubError


class MedScrubClaude:
    """
    Integrated client for safe healthcare AI with Claude

    Automatically de-identifies PHI before sending to Claude API,
    then re-identifies responses to restore original context.

    Attributes:
        medscrub: MedScrub client for PHI de-identification
        claude: Anthropic Claude API client
    """

    def __init__(
        self,
        medscrub_jwt: Optional[str] = None,
        medscrub_api_key: Optional[str] = None,
        claude_api_key: str = None,
        medscrub_api_url: str = "https://api.medscrub.dev",
        claude_model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize integrated MedScrub + Claude client

        Args:
            medscrub_jwt: JWT token from medscrub.dev/demo
            medscrub_api_key: Alternative API key (for local deployment)
            claude_api_key: Anthropic API key (from console.anthropic.com)
            medscrub_api_url: MedScrub API URL (default: hosted)
            claude_model: Claude model to use (default: claude-3-5-sonnet-20241022)
        """
        if not claude_api_key:
            raise ValueError("claude_api_key is required. Get one from console.anthropic.com")

        # Initialize MedScrub client
        self.medscrub = MedScrubClient(
            jwt_token=medscrub_jwt,
            api_key=medscrub_api_key,
            api_url=medscrub_api_url
        )

        # Initialize Claude client
        self.claude = anthropic.Anthropic(api_key=claude_api_key)
        self.model = claude_model

        # Track session for automatic cleanup
        self._current_session_id = None

    def ask_about_fhir(
        self,
        resource: Dict[str, Any],
        question: str,
        session_id: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ask Claude a question about FHIR data with automatic PHI scrubbing

        This method:
        1. De-identifies the FHIR resource using MedScrub
        2. Sends de-identified data + question to Claude
        3. Re-identifies Claude's response to restore original PHI
        4. Returns the answer with full context preserved

        Args:
            resource: FHIR resource (Patient, Observation, etc.) or Bundle
            question: Question to ask Claude about the data
            session_id: Optional session ID (creates new if not provided)
            max_tokens: Maximum tokens in response (default: 1024)
            temperature: Sampling temperature 0-1 (default: 1.0)
            system_prompt: Optional system prompt for Claude

        Returns:
            Dictionary containing:
                - answer: Claude's response with original PHI restored
                - deidentifiedAnswer: Claude's response with tokens
                - sessionId: Session ID for this interaction
                - usage: Token usage stats from Claude
                - processingTime: Total processing time

        Example:
            patient = {
                "resourceType": "Patient",
                "name": [{"family": "Smith", "given": ["John"]}],
                "birthDate": "1985-03-15",
                "condition": [{"code": {"text": "Type 2 Diabetes"}}]
            }

            result = client.ask_about_fhir(
                resource=patient,
                question="What is this patient's diagnosis and when were they born?"
            )

            print(result['answer'])
            # "This patient has Type 2 Diabetes and was born on 1985-03-15."
        """
        import time
        start_time = time.time()

        try:
            # Step 1: De-identify FHIR resource
            deidentify_result = self.medscrub.deidentify_fhir(
                resource=resource,
                session_id=session_id,
                output_format="llm-optimized"  # Human-readable for Claude
            )

            session_id = deidentify_result['sessionId']
            self._current_session_id = session_id
            deidentified_resource = deidentify_result['deidentifiedResource']

            # Step 2: Build prompt for Claude
            default_system = """You are a helpful healthcare AI assistant. You are analyzing de-identified patient data where PHI has been replaced with tokens like [FHIR_NAME_abc123].

Your responses will be automatically re-identified, so use the tokens exactly as shown when referring to patient information.

Provide clear, accurate medical information based on the data provided."""

            user_prompt = f"""Here is the patient data:

{deidentified_resource}

Question: {question}

Please answer the question based on the data provided. Use the exact tokens (e.g., [FHIR_NAME_xyz]) when referring to patient information."""

            # Step 3: Call Claude API
            message = self.claude.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or default_system,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Extract Claude's response
            deidentified_answer = message.content[0].text

            # Step 4: Re-identify Claude's response
            reidentify_result = self.medscrub.reidentify_text(
                text=deidentified_answer,
                session_id=session_id
            )

            original_answer = reidentify_result['reidentifiedText']

            # Calculate total processing time
            total_time = int((time.time() - start_time) * 1000)

            return {
                "answer": original_answer,
                "deidentifiedAnswer": deidentified_answer,
                "sessionId": session_id,
                "usage": {
                    "inputTokens": message.usage.input_tokens,
                    "outputTokens": message.usage.output_tokens,
                    "totalTokens": message.usage.input_tokens + message.usage.output_tokens
                },
                "processingTime": total_time,
                "model": self.model
            }

        except MedScrubError as e:
            raise Exception(f"MedScrub error: {e}")
        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {e}")

    def analyze_fhir_bundle(
        self,
        bundle: Dict[str, Any],
        analysis_prompt: str,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Analyze an entire FHIR Bundle with Claude

        Useful for analyzing a patient's complete medical history,
        multiple resources, or cross-resource patterns.

        Args:
            bundle: FHIR Bundle containing multiple resources
            analysis_prompt: What you want Claude to analyze
            max_tokens: Maximum tokens for response (default: 2048 for longer analysis)

        Returns:
            Dictionary with analysis results (same format as ask_about_fhir)

        Example:
            bundle = {
                "resourceType": "Bundle",
                "entry": [
                    {"resource": patient},
                    {"resource": condition},
                    {"resource": medication_request}
                ]
            }

            result = client.analyze_fhir_bundle(
                bundle=bundle,
                analysis_prompt="Summarize this patient's complete medical history"
            )
        """
        return self.ask_about_fhir(
            resource=bundle,
            question=analysis_prompt,
            max_tokens=max_tokens
        )

    def chat_about_fhir(
        self,
        resource: Dict[str, Any],
        messages: List[Dict[str, str]],
        session_id: Optional[str] = None,
        max_tokens: int = 1024
    ) -> Dict[str, Any]:
        """
        Multi-turn conversation about FHIR data with automatic PHI scrubbing

        Args:
            resource: FHIR resource to discuss
            messages: List of conversation messages [{"role": "user", "content": "..."}]
            session_id: Session ID for consistency (recommended for multi-turn)
            max_tokens: Maximum tokens per response

        Returns:
            Dictionary with conversation response

        Example:
            messages = [
                {"role": "user", "content": "What is this patient's diagnosis?"},
                {"role": "assistant", "content": "[Previous response]"},
                {"role": "user", "content": "What treatment would you recommend?"}
            ]

            result = client.chat_about_fhir(
                resource=patient,
                messages=messages,
                session_id=session_id  # Use same session for context
            )
        """
        import time
        start_time = time.time()

        # De-identify resource once
        deidentify_result = self.medscrub.deidentify_fhir(
            resource=resource,
            session_id=session_id,
            output_format="llm-optimized"
        )

        session_id = deidentify_result['sessionId']
        self._current_session_id = session_id
        deidentified_resource = deidentify_result['deidentifiedResource']

        # Prepend resource context to first user message
        enriched_messages = []
        for i, msg in enumerate(messages):
            if i == 0 and msg['role'] == 'user':
                enriched_content = f"""Patient data:
{deidentified_resource}

{msg['content']}"""
                enriched_messages.append({
                    "role": "user",
                    "content": enriched_content
                })
            else:
                enriched_messages.append(msg)

        # Call Claude with conversation history
        message = self.claude.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=enriched_messages
        )

        deidentified_answer = message.content[0].text

        # Re-identify response
        reidentify_result = self.medscrub.reidentify_text(
            text=deidentified_answer,
            session_id=session_id
        )

        total_time = int((time.time() - start_time) * 1000)

        return {
            "answer": reidentify_result['reidentifiedText'],
            "deidentifiedAnswer": deidentified_answer,
            "sessionId": session_id,
            "usage": {
                "inputTokens": message.usage.input_tokens,
                "outputTokens": message.usage.output_tokens,
                "totalTokens": message.usage.input_tokens + message.usage.output_tokens
            },
            "processingTime": total_time
        }

    def cleanup(self):
        """Delete current session and clear PHI mappings"""
        if self._current_session_id:
            self.medscrub.delete_session(self._current_session_id)
            self._current_session_id = None

    def __enter__(self):
        """Context manager support for automatic cleanup"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatic cleanup on context manager exit"""
        self.cleanup()


# Example usage
if __name__ == "__main__":
    import json
    import os

    # Get credentials from environment
    medscrub_jwt = os.getenv("MEDSCRUB_JWT_TOKEN")
    claude_api_key = os.getenv("ANTHROPIC_API_KEY")

    if not medscrub_jwt or not claude_api_key:
        print("❌ Set MEDSCRUB_JWT_TOKEN and ANTHROPIC_API_KEY environment variables")
        print("\nGet MedScrub JWT: https://medscrub.dev/demo")
        print("Get Claude API key: https://console.anthropic.com")
        exit(1)

    # Example patient with PHI
    patient = {
        "resourceType": "Patient",
        "id": "example-001",
        "name": [{
            "family": "Smith",
            "given": ["John", "Michael"]
        }],
        "birthDate": "1985-03-15",
        "gender": "male",
        "telecom": [{
            "system": "email",
            "value": "john.smith@example.com"
        }],
        "address": [{
            "line": ["123 Main Street"],
            "city": "Boston",
            "state": "MA",
            "postalCode": "02134"
        }]
    }

    # Use context manager for automatic cleanup
    with MedScrubClaude(medscrub_jwt=medscrub_jwt, claude_api_key=claude_api_key) as client:
        print("🏥 MedScrub + Claude Integration Demo\n")
        print("=" * 60)

        # Ask a simple question
        print("\n📋 Question: What is this patient's name and date of birth?")

        result = client.ask_about_fhir(
            resource=patient,
            question="What is this patient's name and date of birth?"
        )

        print(f"\n✅ Claude's Answer:")
        print(result['answer'])
        print(f"\n📊 Usage: {result['usage']['totalTokens']} tokens")
        print(f"⏱️  Processing time: {result['processingTime']}ms")

        # Show that PHI was scrubbed
        print(f"\n🔒 De-identified answer (what Claude actually saw):")
        print(result['deidentifiedAnswer'])

        print(f"\n✨ Session ID: {result['sessionId']}")
        print("(Session automatically cleaned up on exit)")

        print("\n" + "=" * 60)
        print("✅ Demo complete! No PHI was sent to Claude API.")
