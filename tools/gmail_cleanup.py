# Import required Google API libraries
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os.path

# Define required scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Get Gmail service instance"""
    creds = None
    # Check if token file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Create Gmail service instance
    return build('gmail', 'v1', credentials=creds)

def cleanup_emails():
    """Clean up emails from Google Data Studio within the last 5 years"""
    try:
        # Get Gmail service
        service = get_gmail_service()
        
        # Query parameters for Google Data Studio emails within last 5 years
        query = 'from:(looker-studio-noreply@google.com) newer_than:1825d'
        
        print(f'Searching for emails with query: {query}')
        
        # Process all pages of results
        next_page_token = None
        deleted_count = 0
        total_processed = 0
        max_retries = 3
        
        while True:
            try:
                # Get matching emails with pagination
                results = service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=next_page_token
                ).execute()
                
                messages = results.get('messages', [])
                next_page_token = results.get('nextPageToken')
                
                if not messages and total_processed == 0:
                    print('No emails found matching the criteria.')
                    return
                
                total_in_page = len(messages)
                print(f'Processing page with {total_in_page} emails')
                
                # Process each email in the current page
                for message in messages:
                    retry_count = 0
                    while retry_count < max_retries:
                        try:
                            # Get the email content to check subject and from
                            msg = service.users().messages().get(
                                userId='me',
                                id=message['id'],
                                format='metadata',
                                metadataHeaders=['subject', 'from']
                            ).execute()
                            
                            # Get headers
                            headers = msg.get('payload', {}).get('headers', [])
                            subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), '')
                            from_addr = next((header['value'] for header in headers if header['name'].lower() == 'from'), '')
                            
                            print(f'Processing email [{total_processed + 1}] - From: {from_addr}, Subject: {subject}')
                            
                            # Verify it's from Looker Studio
                            if 'looker-studio-noreply@google.com' in from_addr.lower():
                                service.users().messages().trash(
                                    userId='me',
                                    id=message['id']
                                ).execute()
                                deleted_count += 1
                                print(f'Deleted email: {subject}')
                            else:
                                print('Email skipped - Does not match deletion criteria')
                            
                            # If we get here, the operation was successful
                            break
                            
                        except Exception as e:
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f'Error processing message {message["id"]}, attempt {retry_count}/{max_retries}: {str(e)}')
                                import time
                                time.sleep(2 ** retry_count)  # Exponential backoff
                            else:
                                print(f'Failed to process message {message["id"]} after {max_retries} attempts: {str(e)}')
                    
                    total_processed += 1
                    if total_processed % 10 == 0:
                        print(f'Progress: Processed {total_processed} emails, Deleted {deleted_count} emails')
                
                # Break if no more pages
                if not next_page_token:
                    break
                    
            except Exception as page_error:
                print(f'Error processing page: {str(page_error)}')
                break
        
        print(f'Email cleanup completed! Processed {total_processed} emails, Deleted {deleted_count} emails.')
        
    except Exception as error:
        print(f'Error during email cleanup: {error}')
        raise  # Re-raise the exception for better error handling

if __name__ == '__main__':
    cleanup_emails()