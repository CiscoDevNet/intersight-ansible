# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2016 Red Hat Inc.
# (c) 2020 Cisco Systems Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Intersight REST API Module
# Author: Matthew Garrett
# Contributors: David Soper, Chris Gascoigne, John McDonough

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from base64 import b64encode
from email.utils import formatdate
import re
import json
import hashlib
from typing import Optional

from ansible.module_utils.six import iteritems
from ansible.module_utils.six.moves.urllib.parse import urlparse, urlencode
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.basic import env_fallback

try:
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding, ec, rsa
    from cryptography.hazmat.backends import default_backend

    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

intersight_argument_spec = dict(
    api_private_key=dict(fallback=(env_fallback, ['INTERSIGHT_API_PRIVATE_KEY']), type='path', required=True,
                         no_log=True),
    api_uri=dict(fallback=(env_fallback, ['INTERSIGHT_API_URI']), type='str', default='https://intersight.com/api/v1'),
    api_key_id=dict(fallback=(env_fallback, ['INTERSIGHT_API_KEY_ID']), type='str', required=True),
    validate_certs=dict(type='bool', default=True),
    use_proxy=dict(type='bool', default=True),
)


def get_sha256_digest(data):
    """
    Generates a SHA256 digest from a String.

    :param data: data string set by user
    :return: instance of digest object
    """

    digest = hashlib.sha256()
    digest.update(data.encode())

    return digest


def prepare_str_to_sign(req_tgt, hdrs):
    """
    Concatenates Intersight headers in preparation to be signed

    :param req_tgt : http method plus endpoint
    :param hdrs: dict with header keys
    :return: concatenated header authorization string
    """
    ss = ""
    ss = ss + "(request-target): " + req_tgt + "\n"

    length = len(hdrs.items())

    i = 0
    for key, value in hdrs.items():
        ss = ss + key.lower() + ": " + value
        if i < length - 1:
            ss = ss + "\n"
        i += 1

    return ss


def get_gmt_date():
    """
    Generated a GMT formatted Date

    :return: current date
    """

    return formatdate(timeval=None, localtime=False, usegmt=True)


def compare_lists(expected_list, actual_list):
    if len(expected_list) != len(actual_list):
        # mismatch if list lengths aren't equal
        return False
    for expected, actual in zip(expected_list, actual_list):
        # if compare_values returns False, stop the loop and return
        if not compare_values(expected, actual):
            return False
    # loop complete with all items matching
    return True


def compare_values(expected, actual):
    try:
        if isinstance(expected, list) and isinstance(actual, list):
            return compare_lists(expected, actual)
        for (key, value) in iteritems(expected):
            if re.search(r'P(ass)?w(or)?d', key) or key not in actual:
                # do not compare any password related attributes or attributes that are not in the actual resource
                continue
            if not compare_values(value, actual[key]):
                return False
        # loop complete with all items matching
        return True
    except (AttributeError, TypeError):
        # Handle Intersight object references: when expected is a MOID string and actual is an object reference
        if (isinstance(expected, str) and isinstance(actual, dict) and 'Moid' in actual and actual.get('ClassId') == 'mo.MoRef'):
            # Compare the MOID string against the Moid field in the object reference
            if actual['Moid'] == expected:
                return True
        # Handle case where expected is a string and actual is an object reference
        elif (isinstance(expected, str) and isinstance(actual, dict) and
              'Name' in actual and actual.get('ObjectType') == 'organization.Organization'):
            if actual['Name'] == expected:
                return True
        # if expected and actual != expected:
        if actual != expected:
            return False
        return True


# This will fix the format of a v3 secret key, if needed.
# Some v3 keys PEM files are incorrectly formatted with
# "BEGIN EC PRIVATE KEY" instead of "BEGIN PRIVATE KEY"
def _fix_v3_key_format(secret_key: bytes):
    return secret_key.replace(
        b"-----BEGIN EC PRIVATE KEY-----", b"-----BEGIN PRIVATE KEY-----"
    ).replace(b"-----END EC PRIVATE KEY-----", b"-----END PRIVATE KEY-----")


class IntersightModule():

    def __init__(self, module):
        self.module = module
        self.result = dict(changed=False)
        if not HAS_CRYPTOGRAPHY:
            self.module.fail_json(msg='cryptography is required for this module')
        self.host = self.module.params['api_uri']
        self.public_key = self.module.params['api_key_id']
        try:
            with open(self.module.params['api_private_key'], 'r') as f:
                self.private_key = f.read()
        except (FileNotFoundError, OSError):
            self.private_key = self.module.params['api_private_key']
        self.digest_algorithm = ''
        self.response_list = []
        self.update_method = ''

    def get_sig_b64encode(self, data):
        """
        Generates a signed digest from a String

        :param digest: string to be signed & hashed
        :return: instance of digest object
        """
        try:
            key = serialization.load_pem_private_key(self.private_key.encode(), None, default_backend())
        except (ValueError):
            key = serialization.load_pem_private_key(_fix_v3_key_format(self.private_key.encode()), None, default_backend())

        if isinstance(key, rsa.RSAPrivateKey):
            sign = key.sign(data.encode(), padding.PKCS1v15(), hashes.SHA256())
            self.digest_algorithm = 'rsa-sha256'
        elif isinstance(key, ec.EllipticCurvePrivateKey):
            sign = key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
            self.digest_algorithm = 'hs2019'
        else:
            raise Exception("Unsupported key: {0}".format(type(key).__name__))

        return b64encode(sign)

    def get_auth_header(self, hdrs, signed_msg):
        """
        Assmebled an Intersight formatted authorization header

        :param hdrs : object with header keys
        :param signed_msg: base64 encoded sha256 hashed body
        :return: concatenated authorization header
        """

        auth_str = "Signature"

        auth_str = auth_str + " " + "keyId=\"" + self.public_key + "\"," + "algorithm=\"" + self.digest_algorithm + "\","

        auth_str = auth_str + "headers=\"(request-target)"

        for key, dummy in hdrs.items():
            auth_str = auth_str + " " + key.lower()
        auth_str = auth_str + "\""

        auth_str = auth_str + "," + "signature=\"" + signed_msg.decode('ascii') + "\""

        return auth_str

    def call_api(self, **options):
        """
        Call the Intersight API and check for success status
        :param options: options dict with method and other params for API call
        :return: json http response object
        """

        try:
            response, info = self.intersight_call(**options)
            if not re.match(r'2..', str(info['status'])):
                raise RuntimeError(info['status'], info['msg'], info['body'])
        except Exception as e:
            self.module.fail_json(msg="Code exception: %s " % str(e))

        response_data = response.read()
        if len(response_data) > 0:
            resp_json = json.loads(response_data)
            resp_json['trace_id'] = info.get('x-starship-traceid')
            return resp_json
        return {}

    def intersight_call(self, http_method="", resource_path="", query_params=None, body=None, moid=None, name=None):
        """
        Invoke the Intersight API

        :param resource_path: intersight resource path e.g. '/ntp/Policies'
        :param query_params: dictionary object with query string parameters as key/value pairs
        :param body: dictionary object with intersight data
        :param moid: intersight object moid
        :param name: intersight object name
        :return: json http response object
        """

        target_host = urlparse(self.host).netloc
        target_path = urlparse(self.host).path
        query_path = ""
        method = http_method.upper()
        bodyString = ""

        # Verify an accepted HTTP verb was chosen
        if (method not in ['GET', 'POST', 'PATCH', 'DELETE']):
            raise ValueError('Please select a valid HTTP verb (GET/POST/PATCH/DELETE)')

        # Verify the resource path isn't empy & is a valid <str> object
        if (resource_path != "" and not (resource_path, str)):
            raise TypeError('The *resource_path* value is required and must be of type "<str>"')

        # Verify the query parameters isn't empy & is a valid <dict> object
        if (query_params is not None and not isinstance(query_params, dict)):
            raise TypeError('The *query_params* value must be of type "<dict>"')

        # Verify the MOID is not null & of proper length
        if (moid is not None and len(moid.encode('utf-8')) != 24):
            raise ValueError('Invalid *moid* value!')

        if (method != 'PATCH' and self.update_method == 'json-patch'):
            raise ValueError('json-patch is only supported with PATCH on existing resource')

        # Check for query_params, encode, and concatenate onto URL
        if query_params:
            query_path = "?" + urlencode(query_params)

        # Handle PATCH/DELETE by Object "name" instead of "moid"
        if method in ('PATCH', 'DELETE'):
            if moid is None:
                if name is not None:
                    if isinstance(name, str):
                        moid = self.get_moid_by_name(resource_path, name)
                    else:
                        raise TypeError('The *name* value must be of type "<str>"')
                else:
                    raise ValueError('Must set either *moid* or *name* with "PATCH/DELETE!"')

        # Check for moid and concatenate onto URL
        if moid is not None:
            resource_path += "/" + moid

        # Check for GET request to properly form body
        if method != "GET":
            bodyString = json.dumps(body)

        # Concatenate URLs for headers
        target_url = self.host + resource_path + query_path
        request_target = method.lower() + " " + target_path + resource_path + query_path

        # Get the current GMT Date/Time
        cdate = get_gmt_date()

        # Generate the body digest
        body_digest = get_sha256_digest(bodyString)
        b64_body_digest = b64encode(body_digest.digest())

        # Generate the authorization header
        auth_header = {
            'Host': target_host,
            'Date': cdate,
            'Digest': "SHA-256=" + b64_body_digest.decode('ascii'),
        }

        string_to_sign = prepare_str_to_sign(request_target, auth_header)
        b64_signed_msg = self.get_sig_b64encode(string_to_sign)
        auth_header = self.get_auth_header(auth_header, b64_signed_msg)

        # Generate the HTTP requests header
        if self.update_method == 'json-patch':
            content_type = 'application/json-patch+json'
        else:
            content_type = 'application/json'
        request_header = {
            'Accept': 'application/json',
            'Content-Type': content_type,
            'Host': '{0}'.format(target_host),
            'Date': '{0}'.format(cdate),
            'Digest': 'SHA-256={0}'.format(b64_body_digest.decode('ascii')),
            'Authorization': '{0}'.format(auth_header),
        }

        response, info = fetch_url(self.module, target_url, data=bodyString, headers=request_header, method=method,
                                   use_proxy=self.module.params['use_proxy'])

        return response, info

    def get_resource(self, resource_path, query_params, return_list=False):
        '''
        GET a resource and return the 1st element found or the full Results list
        If return_list is False and more than 1 element is returned, a warning is raised
        '''
        options = {
            'http_method': 'get',
            'resource_path': resource_path,
            'query_params': query_params,
        }
        response = self.call_api(**options)
        if response.get('Results'):
            if return_list:
                self.result['api_response'] = response['Results']
            else:
                if len(response['Results']) > 1:
                    self.module.warn('More than 1 resource found, returning the 1st one')
                # return the 1st list element
                self.result['api_response'] = response['Results'][0]
        else:
            # Clear api_response when no results found to prevent returning stale data
            if return_list:
                self.result['api_response'] = []
            else:
                self.result['api_response'] = {}
        self.result['count'] = response.get('Count', 0)
        self.result['trace_id'] = response.get('trace_id')

    def configure_resource(self, moid, resource_path, body, query_params, update_method=''):
        self.update_method = update_method
        if not self.module.check_mode:
            if moid and update_method != 'post':
                # update the resource - user has to specify all the props they want updated
                options = {
                    'http_method': 'patch',
                    'resource_path': resource_path,
                    'body': body,
                    'moid': moid,
                }
                response_dict = self.call_api(**options)
                if response_dict.get('Results'):
                    # return the 1st element in the results list
                    self.result['api_response'] = response_dict['Results'][0]
                    self.result['trace_id'] = response_dict.get('trace_id')
                elif response_dict and 'Moid' in response_dict:
                    # PATCH returned the updated object directly (not in Results array)
                    self.result['api_response'] = response_dict
                    self.result['trace_id'] = response_dict.get('trace_id')
            else:
                # create the resource
                options = {
                    'http_method': 'post',
                    'resource_path': resource_path,
                    'body': body,
                }
                response_dict = self.call_api(**options)
                if response_dict:
                    self.result['api_response'] = response_dict
                    self.result['trace_id'] = response_dict.get('trace_id')
                elif query_params:
                    # POSTs may not return any data.
                    # Get the current state of the resource if query_params.
                    self.get_resource(
                        resource_path=resource_path,
                        query_params=query_params,
                    )
        self.result['changed'] = True

    def delete_resource(self, moid, resource_path):
        # delete resource and create empty api_response
        if not self.module.check_mode:
            options = {
                'http_method': 'delete',
                'resource_path': resource_path,
                'moid': moid,
            }
            resp = self.call_api(**options)
            self.result['api_response'] = {}
            self.result['trace_id'] = resp.get('trace_id')
        self.result['changed'] = True

    def configure_policy_or_profile(self, resource_path, filter_key=None, filter_value=None):
        # Configure (create, update, or delete) the policy or profile
        organization_moid = self.get_moid_by_name(resource_path='/organization/Organizations', resource_name=self.module.params['organization'])

        self.result['api_response'] = {}
        # Get the current state of the resource
        filter_str = "Name eq '" + self.module.params['name'] + "'"
        if filter_value and filter_key:
            filter_str += " and " + filter_key + " eq '" + filter_value + "'"
        try:
            filter_str += "and Organization.Moid eq '" + organization_moid + "'"
        except Exception as e:
            self.module.fail_json(msg="Error getting organization, verify the given organization exists")
        self.get_resource(
            resource_path=resource_path,
            query_params={
                '$filter': filter_str,
                '$expand': 'Organization',
            }
        )

        moid = None
        resource_values_match = False
        if self.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            moid = self.result['api_response']['Moid']
            if self.module.params['state'] == 'present':
                resource_values_match = compare_values(self.api_body, self.result['api_response'])
            else:  # state == 'absent'
                self.delete_resource(
                    moid=moid,
                    resource_path=resource_path,
                )
                moid = None

        if self.module.params['state'] == 'present' and not resource_values_match:
            # remove read-only Organization key
            self.api_body.pop('Organization')
            if not moid:
                # Organization must be set, but can't be changed after initial POST
                self.api_body['Organization'] = {
                    'Moid': organization_moid,
                }
            self.configure_resource(
                moid=moid,
                resource_path=resource_path,
                body=self.api_body,
                query_params={
                    '$filter': filter_str
                }
            )
            if self.result['api_response'].get('Moid'):
                # resource exists and moid was returned
                moid = self.result['api_response']['Moid']

        return moid

    def configure_secondary_resource(self, resource_path, resource_name=None, state='present', custom_filter=None):
        # Configure (create, update, or delete) resources
        # This method is used to configure secondery resources that are part of a policy or profile (e.g. VLANs)

        self.result['api_response'] = {}
        # Get the current state of the resource
        if custom_filter:
            filter_str = custom_filter
        elif resource_name:
            filter_str = "Name eq '" + resource_name + "'"
        else:
            raise ValueError("Either resource_name or custom_filter must be provided")
        self.get_resource(
            resource_path=resource_path,
            query_params={
                '$filter': filter_str
            }
        )

        moid = None
        resource_values_match = False
        if self.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            moid = self.result['api_response']['Moid']
            if state == 'present':
                resource_values_match = compare_values(self.api_body, self.result['api_response'])
            else:  # state == 'absent'
                self.delete_resource(
                    moid=moid,
                    resource_path=resource_path,
                )
                moid = None

        if state == 'present' and not resource_values_match:
            self.configure_resource(
                moid=moid,
                resource_path=resource_path,
                body=self.api_body,
                query_params={
                    '$filter': filter_str
                }
            )
            if self.result['api_response'].get('Moid'):
                # resource exists and moid was returned
                moid = self.result['api_response']['Moid']

        return moid

    def get_moid_by_name(self, resource_path, resource_name) -> Optional[str]:
        '''
        Get the moid of the resource by the value of the resource
        '''
        organization_moid = None
        # GET Moid of the resource
        self.get_resource(
            resource_path=resource_path,
            query_params={
                '$filter': "Name eq '" + resource_name + "'",
                '$select': 'Moid',
            },
        )
        if self.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            return self.result['api_response']['Moid']
        return None

    def get_moid_by_name_and_org(self, resource_path, resource_name, organization_name) -> Optional[str]:
        '''
        Get the moid of an organization-scoped resource by name and organization.

        This function is used for resources that belong to a specific organization
        to avoid conflicts when multiple organizations have resources with the same name.
        '''
        # Get the organization MOID
        org_moid = self.get_moid_by_name(
            resource_path='/organization/Organizations',
            resource_name=organization_name
        )

        if not org_moid:
            self.module.fail_json(msg=f"Organization '{organization_name}' not found")

        # Build filter with both name and organization
        filter_str = f"Name eq '{resource_name}' and Organization.Moid eq '{org_moid}'"

        # GET Moid of the resource
        self.get_resource(
            resource_path=resource_path,
            query_params={
                '$filter': filter_str,
                '$select': 'Moid',
            },
        )

        if self.result['api_response'].get('Moid'):
            # resource exists and moid was returned
            return self.result['api_response']['Moid']
        return None

    def set_query_params(self, filter_key=None, filter_value=None) -> dict:
        filter_conditions = []
        name_to_filter = self.module.params.get('name')
        org_to_filter = self.module.params.get('organization')
        if name_to_filter:
            filter_conditions.append(f"Name eq '{name_to_filter}'")

        if org_to_filter:
            org_moid = self.get_moid_by_name(resource_path='/organization/Organizations', resource_name=org_to_filter)
            filter_conditions.append(f"Organization.Moid eq '{org_moid}'")

        if filter_value and filter_key:
            filter_conditions.append(f"'{filter_key}' eq '{filter_value}'")

        query_params = {}
        if filter_conditions:
            query_params["$filter"] = " and ".join(filter_conditions)
        return query_params

    def set_tags_and_description(self):
        """
        Generalize the pattern of setting tags and description in api_body if they are provided in module params.
        """
        if self.module.params.get('tags'):
            self.api_body['Tags'] = self.module.params['tags']
        if self.module.params.get('description'):
            self.api_body['Description'] = self.module.params['description']
