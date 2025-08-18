from datetime import datetime
import re
from pymongo.collection import Collection
class EmotionalIssue:
    """Store and retrieve emotional issues from MongoDB."""

    def __init__(self, collection: Collection):
        self.collection = collection

    def store_issue(
            self,
            user_id: str,
            issue_type: str,
            description: str,
            severity: str = "medium") -> str:
        
        """Store an emotional issue in MongoDB.

        WHEN TO STORE ISSUES:
        - When user expresses persistent emotional distress (lasting more than a few days)
        - When user mentions specific mental health concerns (anxiety, depression, etc.)
        - When user describes significant life problems affecting their wellbeing
        - When user asks for help with recurring emotional patterns
        - When user mentions feeling overwhelmed, hopeless, or unable to cope

        DO NOT STORE:
        - Temporary bad moods or daily frustrations
        - Minor complaints without emotional impact
        - General chitchat or casual conversation
        - Issues already stored in the same conversation

        Args:
            user_id: Unique identifier for the user (required for all storage operations)
            issue_type: Type of emotional issue (anxiety, depression, stress, etc.)
            description: Detailed description of the issue
            severity: Severity level (low, medium, high)

        Returns:
            Confirmation message
        """
        try:
            if severity.lower() == "low":
                return f"The user's emotion is {issue_type.upper()}. Let's the music does its job!"
            issue_document = {
                "user_id": user_id,
                "issue_type": issue_type.lower(),
                "description": description,
                "severity": severity.lower(),
                "timestamp": datetime.utcnow(),
                "status": "active",
                "resolution_notes": []
            }

            result = self.collection.insert_one(issue_document)

            return f"The user's emotion is {issue_type.upper()} and recorded successfully (ID: {str(result.inserted_id)}). Let's the music does its job!"
        except Exception as e:
            return f"Unable to store issue: {str(e)}. But I'm still here to talk and support you."

    def get_user_issues(self, user_id: str) -> str:
        """Retrieve stored emotional issues for a user.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Summary of user's stored issues
        """
        try:

            issues = list(self.collection.find(
                {"user_id": user_id}).sort("timestamp", -1))

            if not issues:
                return "No previous issues found in your record."

            summary = f"Found {len(issues)} previous issue(s):\n"
            for issue in issues[:5]:  # Show last 5 issues
                summary += f"• {issue['issue_type'].title()}: {issue['description'][:100]}... (Status: {issue['status']})\n"

            return summary

        except Exception as e:
            return f"Unable to retrieve issues: {str(e)}"
        
    def delete_issue(self, issue_type: str) -> str:
        """Delete an emotional issue of the given type.

        Args:
            issue_type: Unique identifier for the issue to delete

        Returns:
            Success message if issue deleted or not found
        """
        
        try:
            result = self.collection.delete_one({"issue_type": issue_type})
            if result.deleted_count:
                return "Issue deleted successfully."
            else:
                return "Issue not found."
        except Exception as e:
            return f"Unable to delete issue: {str(e)}"
        
    def modified_severity(self, issue_type: str, change: str):
        
        """Update the severity of an emotional issue.

        Args:
            issue_type: Unique identifier for the issue to update
            change: New severity level (low, medium, high)

        Returns:
            Success message if issue updated or not found
        """
        try:
            result = self.collection.update_many(
                {"issue_type": issue_type},
                {"$set": {"severity": change}}
            )
            if result.modified_count:
                return "Issue severity updated successfully."
            else:
                return "Issue not found."
        except Exception as e:
            return f"Unable to update issue severity: {str(e)}"

    def modified_status(self, issue_type: str, change: str):
        
        """Update the status of an emotional issue.

        Args:
            issue_type: Unique identifier for the issue to update
            change: New status for the issue (active, inactive, resolved)

        Returns:
            Success message if issue updated or not found
        """
        try:
            normalized = re.sub(r'\s+', r'\\s*', issue_type.strip())
            regex = f"^{normalized}$"

            result = self.collection.update_many(
                {"issue_type": {"$regex": regex, "$options": "i"}},
                {"$set": {"status": change}}
            )
            if result.modified_count:
                return "Issue status updated successfully."
            else:
                return "Issue not found."
        except Exception as e:
            return f"Unable to update issue status: {str(e)}"