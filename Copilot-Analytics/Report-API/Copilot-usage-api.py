import requests
from msal import ConfidentialClientApplication
import json
import csv

# Replace with your values
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
tenant_id = "YOUR_TENANT_ID"
period = "D7"  # Change as needed: D7, D30, D90, D180, ALL

# MS Graph endpoints
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]
endpoint = f"https://graph.microsoft.com/beta/reports/getMicrosoft365CopilotUsageUserDetail(period='{period}')"

# Get token
app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

token_response = app.acquire_token_for_client(scopes=scope)

if "access_token" in token_response:
    access_token = token_response["access_token"]
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        print("Success!")
        
        # Parse JSON response
        try:
            data = response.json()
            print("API Response structure:")
            print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Extract the value array which contains the user data
            if 'value' in data:
                users_data = data['value']
                print(f"Found {len(users_data)} users")
                
                # Process each user's data
                filtered_rows = []
                for user in users_data:
                    # Extract basic user info
                    filtered_row = {
                        "UserPrincipalName": user.get("userPrincipalName", ""),
                        "DisplayName": user.get("displayName", ""),
                        "ReportRefreshDate": user.get("reportRefreshDate", ""),
                        "LastActivityDate": user.get("lastActivityDate", ""),
                        "CopilotChatLastActivityDate": user.get("copilotChatLastActivityDate", ""),
                        "WordCopilotLastActivityDate": user.get("wordCopilotLastActivityDate", ""),
                        "ExcelCopilotLastActivityDate": user.get("excelCopilotLastActivityDate", ""),
                        "PowerPointCopilotLastActivityDate": user.get("powerPointCopilotLastActivityDate", ""),
                        "OutlookCopilotLastActivityDate": user.get("outlookCopilotLastActivityDate", ""),
                        "OneNoteCopilotLastActivityDate": user.get("oneNoteCopilotLastActivityDate", ""),
                        "LoopCopilotLastActivityDate": user.get("loopCopilotLastActivityDate", ""),
                        "MicrosoftTeamsCopilotLastActivityDate": user.get("microsoftTeamsCopilotLastActivityDate", "")
                    }
                    
                    # Extract activity details if available
                    if "copilotActivityUserDetailsByPeriod" in user and user["copilotActivityUserDetailsByPeriod"]:
                        activity_details = user["copilotActivityUserDetailsByPeriod"][0]  # Take first period
                        filtered_row.update({
                            "ReportPeriod": activity_details.get("reportPeriod", ""),
                            "CopilotChatMessages": activity_details.get("copilotChatMessages", ""),
                            "CopilotUsed": activity_details.get("copilotUsed", "")
                        })
                    else:
                        filtered_row.update({
                            "ReportPeriod": "",
                            "CopilotChatMessages": "",
                            "CopilotUsed": ""
                        })
                    
                    filtered_rows.append(filtered_row)
                
                # Export to CSV file
                if filtered_rows:
                    output_file = "copilot_usage_report.csv"
                    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=filtered_rows[0].keys())
                        writer.writeheader()
                        writer.writerows(filtered_rows)
                    print(f"\n✅ Exported {len(filtered_rows)} user records to {output_file}")
                    
                    # Display sample data
                    print("\nSample data (first 3 rows):")
                    for i, row in enumerate(filtered_rows[:3]):
                        print(f"Row {i+1}: {row}")
                else:
                    print("No user data found to export")
            else:
                print("No 'value' key found in response")
                print("Response data:", json.dumps(data, indent=2)[:500] + "...")
        
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print("Response content:", response.text[:500] + "...")
        except Exception as e:
            print(f"Error processing data: {e}")
            
    else:
        print(f"Failed: {response.status_code}")
        print("Response:", response.text)
else:
    print("Token acquisition failed:")
    print(token_response.get("error_description"))
