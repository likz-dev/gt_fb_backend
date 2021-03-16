import json
from unittest import mock

from mock import MagicMock, patch


def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'status': 'ok'}
    assert json.loads(res.get_data(as_text=True)) == expected


@mock.patch('authlib.integrations.flask_client.remote_app.FlaskRemoteApp.authorize_redirect', return_value=('', 302))
def test_login(mock_authorize_redirect, app, client):
    res = client.get('/login')
    mock_authorize_redirect.assert_called_once()
    assert res.status_code == 302


@mock.patch('authlib.integrations.flask_client.remote_app.FlaskRemoteApp.authorize_access_token',
            return_value={'access_token': 'y-oFK48VbGYd14btAF6Qk46nEsop3R-M',
                          'id_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Indrcy1UNUVkek44UnpJY0FUVnVwbCJ9.eyJuaWNrbmFtZSI6InRlc3QiLCJuYW1lIjoidGVzdEB0ZXN0LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9iNjQyYjQyMTdiMzRiMWU4ZDNiZDkxNWZjNjVjNDQ1Mj9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnRlLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDIxLTAzLTE2VDA1OjQ4OjE5LjU1OVoiLCJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vZGV2LXZ3MGVhanJxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDUwMjdmNmRmZWM4YTAwNjk2MDZiM2UiLCJhdWQiOiJXSVI1dmpJWk5ncEY0UjVqNGE5cGMzb2VmdzU2N0hCeCIsImlhdCI6MTYxNTg4NTY3OSwiZXhwIjoxNjE1OTIxNjc5LCJub25jZSI6IndLMWVkZzNDOFp2QzZQcmxNVkpWIn0.E1i7pibcznccod5OzLnGugPcaX_85Ip_gg6AVlCh1pHCFOTsw_QGV9xWC4Ut1us_NJQHRh4tcywfvoKG5p3ukpoSF2M8mk8Obz2YReD6Zt5wlEq7jFfxIUy4Dk9R9qF3BOyJhYT_ZySHoQqhircecpSKR8J5XWj71t0pkUS-0ypTsgkR8pq3GeC8C9LfF17LOh8y59ChB4nsPYkljDG5JJMghLVrHi1rdlFlHFn8S7uzcAckSI_x_Ae_qv7I_u8TSd626TUuukkC6r-QVX-Yuo1FFGjoJsO_C4l8FlHrrLZNN-LfT0AMn7WivvqbSlz0S-CpWoVqQTTg1Nc02Ly6Cg',
                          'scope': 'openid profile email', 'expires_in': 86400, 'token_type': 'Bearer',
                          'expires_at': 1615972078})
def test_callback(mock_authorize_access_token, app, client):
    mock_resp = MagicMock()
    mock_resp.json = MagicMock(
        return_value={'sub': 'auth0|605027f6dfec8a0069606b3e', 'nickname': 'test', 'name': 'test@test.com',
                      'picture': 'https://s.gravatar.com/avatar/b642b4217b34b1e8d3bd915fc65c4452?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fte.png',
                      'updated_at': '2021-03-16T05:48:19.559Z', 'email': 'test@test.com', 'email_verified': False}
        )
    with patch('authlib.integrations.flask_client.remote_app.FlaskRemoteApp.get', return_value=mock_resp) as mock_get:
        res = client.get('/callback')
        mock_authorize_access_token.assert_called_once()
        assert res.status_code == 302
