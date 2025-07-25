# Microsoft Graph API – Permissions & Setup Guide

## 1. Microsoft Entra App Registration

To authenticate and access Microsoft Graph API, you’ll need the following credentials from your app registration in Microsoft Entra:

- `client_id`
- `client_secret`
- `tenant_id`
- Required API permissions

### Application Permission Required:

- **Reports.Read.All**  
  > This is an application-level permission and must be **admin-consented**.

---

## 2. Key Resources

- **API Documentation**  
  🔗 [getMicrosoft365CopilotUsageUserDetail](https://learn.microsoft.com/en-us/graph/api/reportroot-getmicrosoft365copilotusageuserdetail?view=graph-rest-beta&tabs=http)

- **User Anonymization**  
  By default, user details such as display name and email are anonymized in this report. This behavior follows your tenant’s privacy settings.  
  To show identifiable information, refer to this guide:  
  🔗 [Show user, group, or site details in reports](https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/activity-reports?view=o365-worldwide&WT.mc_id=365AdminCSH_inproduct#show-user-group-or-site-details-in-the-reports)

---

## 3. Security Notes

- The `Reports.Read.All` permission grants access to organization-wide reporting data, including usage insights.
- Ensure best practices for secure implementation:
  - Keep client credentials (`client_secret`) safe and never expose them in public repositories.
  - Use secure storage solutions like **Azure Key Vault**.
  - Limit access to the app registration and its credentials to authorized personnel only.
