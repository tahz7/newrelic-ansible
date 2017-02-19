# newrelic-ansible

### description:

Using ansible the script will install and activate newrelic on both centos/redhat and ubuntu/debian machines. Arguments include providing the newrelic user/pass or the newrelic licence key to activate the installation.

Note: the installation will skip if newrelic already exists on the target host.

### usage: 
```
ansible-playbook --extra-vars '{"LICENCE":"licence-key"}' mail.yml
```
or you can scrape the licence key (not recommended and should only be done on test accounts):
```
ansible-playbook --extra-vars '{"USER":"username","PASS":"password"}' main.yml
```
### TO-DO:

* Add php integration option
