def company_detail(client, account, company_id: int):
    return client.get(f"/companies/api/v1/detail/{company_id}", headers=account.headers)


def update_company(client, account, company_id: int, **fields):
    return client.patch(
        f"/companies/api/v1/update/{company_id}", json=fields, headers=account.headers
    )
