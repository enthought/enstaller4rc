import base64
import re

from attr import attr, attributes
from six.moves import urllib

from .errors import Enstaller4rcError


_DEFAULT_PORT = 3128
_PORT_PROG_R = re.compile('^(.*):([0-9]+)$')
_PASSWD_PROG_R = re.compile('^([^:]*):(.*)$', re.S)


@attributes
class UserPasswordAuth(object):
    """ Simple clear text username/password authentication."""
    username = attr()
    password = attr()

    @classmethod
    def from_encoded_auth(cls, encoded_auth):
        parts = (
            base64.decodestring(encoded_auth.encode("utf8")).
            decode("utf8").
            split(":")
        )

        if len(parts) == 2:
            return cls(*parts)
        else:
            raise ValueError("Invalid auth line")


@attributes
class APITokenAuth(object):
    token = attr()


@attributes
class OldStyleRepositoryConfiguration(object):
    store_url = attr()


@attributes
class CanopyRepositoryConfiguration(object):
    store_url = attr()
    use_pypi = attr(default=False)


@attributes
class BroodRepositoryConfiguration(object):
    store_url = attr()
    name = attr()


@attributes
class FSRepositoryConfiguration(object):
    store_url = attr()


@attributes
class ProxyConfiguration(object):
    host = attr()
    scheme = attr(default="http")
    port = attr(default=3128)
    user = attr(default="")
    password = attr(default="")

    @classmethod
    def from_string(cls, s):
        parts = urllib.parse.urlparse(s)
        if len(parts.scheme) > 0:
            scheme = parts.scheme
        else:
            scheme = "http"

        if len(parts.netloc) == 0:
            if len(parts.path) > 0:
                # this is to support url such as 'acme.com:3128'
                netloc = parts.path
            else:
                msg = "Invalid proxy string {0!r} (no host found)".format(s)
                raise Enstaller4rcError(msg)
        else:
            netloc = parts.netloc

        userpass, hostport = urllib.parse.splituser(netloc)
        if userpass is None:
            user, password = "", ""
        else:
            user, password = _splitpasswd(userpass)
            password = password or ""

        host, port = _splitport(hostport)
        if port is None:
            port = _DEFAULT_PORT
        else:
            port = int(port)

        if len(host) == 0:
            msg = "Invalid proxy string {0!r} (no host found)"
            raise Enstaller4rcError(msg.format(s))

        return cls(host, scheme, port, user, password)

    def __str__(self):
        netloc = "{0}:{1}".format(self.host, self.port)

        if self.user:
            netloc = "{0}:{1}@{2}".format(self.user, self.password, netloc)

        return urllib.parse.urlunparse((self.scheme, netloc, "", "", "", ""))


# Looks like those are semi-private function in the stdlib, so we bundle it
# here for 2/3 compat
def _splitport(host):
    match = _PORT_PROG_R.match(host)
    if match:
        return match.group(1, 2)
    else:
        return host, None


def _splitpasswd(user):
    match = _PASSWD_PROG_R.match(user)
    if match:
        return match.group(1, 2)
    else:
        return user, None