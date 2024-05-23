import requests

def aci_login(base_url, username, password):
    """ Log into Cisco ACI and return the session token. """
    login_url = f"{base_url}/api/aaaLogin.json"
    json_login_credentials = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": password
            }
        }
    }
    try:
    
        response = requests.post(login_url, json=json_login_credentials, verify=False)
        response.raise_for_status()
        token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
        return token
    except requests.exceptions.HTTPError as err:
        if response.status_code == 403:
            print("Access denied. Check your username and password, and ensure your account has the necessary permissions.")
        else:
            print(f"HTTP Error occurred: {response.status_code} - {err}")
        return None
    
def get_tenants(base_url, token):
    """ Retrieve all tenants. """
    tenant_url = f"{base_url}/api/node/class/fvTenant.json"
    print(tenant_url)
    headers = {'APIC-cookie': token}
    response = requests.get(tenant_url, headers=headers, verify=False)
    response.raise_for_status()
    tenants = response.json()["imdata"]
    return [tenant["fvTenant"]["attributes"]["name"] for tenant in tenants]

def find_bd_with_vlan(base_url, token, vlan_id):
    """ Search through all Bridge Domains in all tenants to find the specified VLAN ID. """
    tenants = get_tenants(base_url, token)
    print(tenants)
    for tenant in tenants:
        bd_url = f"{base_url}/api/node/mo/uni/tn-{tenant}.json?query-target=subtree&target-subtree-class=fvBD"
        headers = {'APIC-cookie': token}
        response = requests.get(bd_url, headers=headers, verify=False)
        response.raise_for_status()
        bds = response.json()["imdata"]
        for bd in bds:
            if bd["fvBD"]["attributes"]["seg"] == str(vlan_id):
                return bd["fvBD"]["attributes"]["name"], tenant
    return None, None
