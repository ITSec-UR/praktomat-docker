#!/bin/bash
echo -n | openssl s_client -connect ldap.uni-regensburg.de:636 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | tee ldapserver.pem