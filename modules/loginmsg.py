#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: loginmsg

short_description: This is my test module

version_added: "2.4"

description:
    - "This is my longer description explaining my test module"

options:
    name:
        description:
            - This is the message to send to the test module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

author:
    - Your Name (@Jeroenvdl)
'''

EXAMPLES = '''
---
- name: set up login messages
  hosts: all
  collections:
   - <my_namespace>.loginmsg
  become: yes
  tasks:
  - name: put a logon message before logging in
    loginmsg:
      text: Hello, you are entering a Hackathon Machine!
      when: before
      fqdn: true
      state: present
 
  - name: put a logon message after logging in
    loginmsg:
      text: Hi there, welcome in a Hackathon Machine!
      when: after
      fqdn: true
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

import socket
import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        text=dict(type='str', required=True),
        when=dict(type='str', required=True, choises=['before', 'after']),
        fqdn=dict(type='bool', required=False, default=False),
        state=dict(type='str', required=False, default='present', choices=['absent', 'present'])

    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    ) 

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.params['when'] == "before":
        filename = '/etc/issue'
    elif module.params['when'] == "after":
        filename = '/etc/motd'
    else:
        module.exit_json(**result)

    if module.params['state'] == 'present' and module.params['fqdn'] == True:
        with open(filename, 'w') as file_object:
            message = module.params['text'] + " " + socket.getfqdn()
            file_object.write(message)
        
        result['changed'] = True
    else:
        with open(filename, 'w') as file_object:
            message = module.params['text']
            file_object.write(message)
        
        result['changed'] = True
    
    if module.params['state'] == 'absent':
        try:
            with open(filename) as file_object:
                os.remove(filename)
                result['changed'] = True
        except FileNotFoundError:
            print(filename + "Not Found.")
            result['changed'] = False

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()