# GAE-friendly Chef API Client

This library implements a thin wrapper around the [Chef server API](https://docs.chef.io/api_chef_server.html) using only PyCrypto functions for RSA signing.

## Installation
We're on pypi:
```
pip install chef_gae
```
## Usage/Samples
See code examples below.

You can find a list of endpoints on the [Chef server API](https://docs.chef.io/api_chef_server.html) docs.

###Get all nodes
```python
from gae_chef import Chef

rsa_key = open('chef_client_key.pem').read()
client = Chef(server_url=chef_server_url,
              rsa_key=rsa_key,
              chef_username=chef_username,
              org_name=your_org_name)

#create a node
nodes = client.get_endpoint('GET', '/nodes')

#return value is a dictionary
for node in nodes:
    print node['name']
```

###Create a Node
```python
from gae_chef import Chef

rsa_key = open('chef_client_key.pem').read()
client = Chef(server_url=chef_server_url,
              rsa_key=rsa_key,
              chef_username=chef_username,
              org_name=your_org_name)

#data arg is a JSON-serialiazble dictionary
node_data = {'name': 'hello'}
new_node = client.get_endpoint('POST', '/nodes', data=node_data)
print new_node['uri']
```

###Update a node
WARNING: The Chef Server API is finicky about accepting updates. If you're planning to PUT data (eg updating a node), you'll probably want to GET the current status, then PUT the resulting object back. Example below:
```python
from gae_chef import Chef

rsa_key = open('chef_client_key.pem').read()
client = Chef(server_url=chef_server_url,
              rsa_key=rsa_key,
              chef_username=chef_username,
              org_name=your_org_name)

#get node first
node = client.get_endpoint('GET', '/nodes/hello')
#set some attribute from returned data
node['normal']['cool_users'] = ['ariel', 'christian', 'michael']

#update with modified returned data
client.get_endpoint('PUT', '/nodes/hello', data=node)
```

You can also hit undocumented endpoints, like the ones surrounding access control. Same warning as above applies if you plan to update access control:
```python
from gae_chef import Chef
rsa_key = open('chef_client_key.pem').read()

client = Chef(server_url=chef_server_url,
              rsa_key=rsa_key,
              chef_username=chef_username,
              org_name=your_org_name)
access_list = client.get_endpoint('GET', '/nodes/hello/_acl')
```
