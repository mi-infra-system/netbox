# Authentication

## Local Authentication

Local user accounts and groups can be created in NetBox under the "Authentication" section in the "Admin" menu.

At a minimum, each user account must have a username and password set. User accounts may also denote a first name, last name, and email address. [Permissions](../permissions.md) may also be assigned to individual users and/or groups as needed.

## Remote Authentication

NetBox may be configured to provide user authenticate via a remote backend in addition to local authentication. This is done by setting the `REMOTE_AUTH_BACKEND` configuration parameter to a suitable backend class. NetBox provides several options for remote authentication.

### LDAP Authentication

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.LDAPBackend'
```

NetBox includes an authentication backend which supports LDAP. See the [LDAP installation docs](../../installation/6-ldap.md) for more detail about this backend.

### HTTP Header Authentication

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.RemoteUserBackend'
```

Another option for remote authentication in NetBox is to enable HTTP header-based user assignment. The front end HTTP server (e.g. nginx or Apache) performs client authentication as a process external to NetBox, and passes information about the authenticated user via HTTP headers. By default, the user is assigned via the `REMOTE_USER` header, but this can be customized via the `REMOTE_AUTH_HEADER` configuration parameter.

Optionally, user profile information can be supplied by `REMOTE_USER_FIRST_NAME`, `REMOTE_USER_LAST_NAME` and `REMOTE_USER_EMAIL` headers. These are saved to the user's profile during the authentication process. These headers can be customized like the `REMOTE_USER` header.

!!! warning Verify Header Compatibility
    Some WSGI servers may drop headers which contain unsupported characters. For instance, gunicorn v22.0 and later silently drops HTTP headers containing underscores. This behavior can be disabled by changing gunicorn's [`header_map`](https://docs.gunicorn.org/en/stable/settings.html#header-map) setting to `dangerous`.
