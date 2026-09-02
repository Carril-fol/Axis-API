from tests.companies.conftest import company_detail, update_company


def test_the_owner_reads_and_updates_their_company(client, owner):
    response = update_company(
        client, owner, owner.company_id, address="742 Evergreen Terrace"
    )

    assert response.status_code == 200
    detail = company_detail(client, owner, owner.company_id)
    assert detail.get_json()["company"]["address"] == "742 EVERGREEN TERRACE"


def test_a_member_is_refused(client, owner, member):
    response = company_detail(client, member, owner.company_id)

    assert response.status_code == 403


def test_another_owner_is_refused(client, owner, other_company):
    response = company_detail(client, other_company, owner.company_id)

    assert response.status_code == 403
