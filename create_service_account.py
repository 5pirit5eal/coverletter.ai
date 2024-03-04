import os

from google.oauth2 import service_account  # type: ignore
import googleapiclient.discovery  # type: ignore

def create_service_account(project_id: str, name: str, display_name: str) -> dict:
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = googleapiclient.discovery.build("iam", "v1", credentials=credentials)

    my_service_account = (
        service.projects()
        .serviceAccounts()
        .create(
            name="projects/" + project_id,
            body={"accountId": name, "serviceAccount": {"displayName": display_name}},
        )
        .execute()
    )

    print("Created service account: " + my_service_account["email"])
    return my_service_account

