"""
Google Calendar Service for creating events with Google Meet links
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for Google Calendar API
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

class GoogleCalendarService:
    """Service for interacting with Google Calendar API"""
    
    def __init__(self, credentials_path: str = "credentials.json"):
        self.credentials_path = credentials_path
        self.token_path = "token.json"
        self.credentials = None
        self.service = None
    
    def get_authorization_url(self, redirect_uri: str) -> str:
        """Get the authorization URL for OAuth flow"""
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        return authorization_url
    
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Save credentials for future use
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        with open(self.token_path, 'w') as token_file:
            json.dump(token_data, token_file)
        
        return token_data
    
    def load_credentials(self) -> bool:
        """Load credentials from token file"""
        if os.path.exists(self.token_path):
            with open(self.token_path, 'r') as token_file:
                token_data = json.load(token_file)
                self.credentials = Credentials(
                    token=token_data['token'],
                    refresh_token=token_data.get('refresh_token'),
                    token_uri=token_data['token_uri'],
                    client_id=token_data['client_id'],
                    client_secret=token_data['client_secret'],
                    scopes=token_data['scopes']
                )
                return True
        return False
    
    def build_service(self):
        """Build the Google Calendar service"""
        if self.credentials:
            self.service = build('calendar', 'v3', credentials=self.credentials)
            return True
        return False
    
    def create_event_with_meet(
        self,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        attendee_emails: list = None,
        timezone: str = "Africa/Nairobi"
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Google Calendar event with Google Meet link
        
        Args:
            title: Event title
            description: Event description
            start_time: Event start time
            end_time: Event end time
            attendee_emails: List of attendee email addresses
            timezone: Timezone for the event
            
        Returns:
            Dictionary with event details including meet_link and event_id
        """
        if not self.service:
            if not self.load_credentials():
                return None
            if not self.build_service():
                return None
        
        # Create event body
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': timezone,
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f"skillswap-{start_time.timestamp()}",
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 30},
                ],
            },
        }
        
        # Add attendees if provided
        if attendee_emails:
            event['attendees'] = [{'email': email} for email in attendee_emails]
        
        try:
            # Create the event with conference data
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1,
                sendUpdates='all' if attendee_emails else 'none'
            ).execute()
            
            # Extract meet link
            meet_link = None
            if 'conferenceData' in created_event:
                entry_points = created_event['conferenceData'].get('entryPoints', [])
                for entry in entry_points:
                    if entry.get('entryPointType') == 'video':
                        meet_link = entry.get('uri')
                        break
            
            return {
                'event_id': created_event.get('id'),
                'meet_link': meet_link,
                'html_link': created_event.get('htmlLink'),
                'status': 'created'
            }
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {
                'error': str(error),
                'status': 'failed'
            }
    
    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event"""
        if not self.service:
            if not self.load_credentials():
                return False
            if not self.build_service():
                return False
        
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True
        except HttpError:
            return False


# Global instance
google_calendar_service = GoogleCalendarService()
