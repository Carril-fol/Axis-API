def refresh(client, refresh_token: str):
    return client.post(
        "/auth/api/v1/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
