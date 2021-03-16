from unittest import mock

import pytest
from jose import jwt
from mock import patch

from app.views.helpers.authentication import get_token_auth_header, AuthError, authenticate


@pytest.mark.parametrize('header,code,description,response_code', [
    ('', 'authorization_header_missing', 'Authorization header is expected', 401),
    ('ABC', 'invalid_header', 'Authorization header must start with Bearer', 401),
    ('Bearer', 'invalid_header', 'Token not found', 401),
    ('Bearer abc def', 'invalid_header', 'Authorization header must be Bearer token', 401)
])
def test_get_token_auth_header_invalid(header, code, description, response_code):
    with pytest.raises(AuthError) as auth_error:
        with patch('app.views.helpers.authentication.get_authorization_header', return_value=header):
            get_token_auth_header()
    assert auth_error.value.args[0].get('code') == code
    assert auth_error.value.args[0].get('description') == description
    assert auth_error.value.args[1] == response_code


def test_get_token_auth_header_valid():
    with patch('app.views.helpers.authentication.get_authorization_header', return_value='Bearer valid_token'):
        token = get_token_auth_header()
        assert token == 'valid_token'


@mock.patch('jose.jwt.decode')
@mock.patch('jose.jwt.get_unverified_header',
            return_value={'alg': 'RS256', 'typ': 'JWT', 'kid': 'wks-T5EdzN8RzIcATVupl'})
@mock.patch('app.views.helpers.authentication.get_well_known_jwks',
            return_value='{"keys":[{"alg":"RS256","kty":"RSA","use":"sig","n":"kJ5itI5Rf5dE_UMmTCdi8NQbljgHWgU9615y_F8Hd9PWg_2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A_38h42fBwJjXfa3_KrvLXm5i-KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0-riHmgkVmIMpRY0fwnEz4wvjqoi-A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh-Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposw","e":"AQAB","kid":"wks-T5EdzN8RzIcATVupl","x5t":"Dk0ateKMS5FGXXIlJaStmqXxMxg","x5c":["MIIDDTCCAfWgAwIBAgIJKb8AZYZ1HwB9MA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJ5itI5Rf5dE/UMmTCdi8NQbljgHWgU9615y/F8Hd9PWg/2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A/38h42fBwJjXfa3/KrvLXm5i+KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0+riHmgkVmIMpRY0fwnEz4wvjqoi+A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh+Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSm8T/8EM4Bc6/U9XPE0o5TEOB3CDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAIlbQkA/BVjdE8QQs3jjKQbxVayemFa4usES4u76S90NkKAiP7v6ZuxBlVsHIDXbAxwPNa6h9yLvZU9EyELjnG0y3y/ja044b0mIyO9q7vvg97ttKCDvuNytaGuxj4TBYzEcCP/krll3DMWviVuwxTRoh/UNHS8tHqhEhFx9AKidc1k0S6+ltv5nOHZXn7BvX0tmILuaC45D4qHb+ZJDmguYGQBPtZhnx3NO7QfVF8Veu9uGqG2VqSzGMQaVLq90dUQKM3hpjffkpRKEtetFHYykLWpMyk2FKfN2yVpSl4JFlJxFsLNuBqYPk5PuHCxdhytayzXoqU644ZfFbnToOf4="]},{"alg":"RS256","kty":"RSA","use":"sig","n":"wIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1-j1USJVg-lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL_OxCFltHpNcFSOYXIhd-AacxQ6JLMZWYmXxAhI_k7CuDYulXH69hPz-qJFXcV-iFAMlzI-wYCm-5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN-g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQ","e":"AQAB","kid":"9nMOM4cMNY2BKpHNxpKf8","x5t":"O5k8zyePYH8wZofBVxBjgSDa1ZY","x5c":["MIIDDTCCAfWgAwIBAgIJPYHFYGfDrZ2xMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1+j1USJVg+lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL/OxCFltHpNcFSOYXIhd+AacxQ6JLMZWYmXxAhI/k7CuDYulXH69hPz+qJFXcV+iFAMlzI+wYCm+5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN+g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQBYXJM7mOlRCcps11/fY9dRgvLRjAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKQSDk1bXVlna1cSddh5Wut0v+RXWmffj409Pso15Yw6roVfp7bVSh1LyN3O0ETky5UuK3nHXxpkSA2Bs7wCwQ+aXC4vKYLf3NTzXzkEdJ/S6ZtZT0Gm8zL83GLYrIf6X9r1O73TTcS2/8KxxolPQB6+uj4N345+Gf6sHsjJd2lNJv485hLpn/DpeyzNM3r/IkyPMCuIv/Icitj4xXpkJ6p0kUZ4psLHoWbpFj/syjSTrgMeY+9oRXLYDZEr30tcXet8LXOr4EAV0Z79Z66A4FyUmkQJiESuJkd9VrMFJkmiDr4nds/5E6YZYk8m9n6TO9+ZHUn9UqtI71GfZdsqiU8="]}]}')
@mock.patch('app.views.helpers.authentication.get_token_auth_header', return_value='token')
def test_authenticate_valid(_a, _b, _c, _d):
    result = authenticate()
    assert result is True


@pytest.mark.parametrize('error,code,description,response_code', [
    (jwt.ExpiredSignatureError, 'token_expired', 'token is expired', 401),
    (jwt.JWTClaimsError, 'invalid_claims', 'incorrect claims,please check the audience and issuer', 401),
    (Exception, 'invalid_header', 'Unable to parse authentication token.', 401)
])
@mock.patch('jose.jwt.get_unverified_header',
            return_value={'alg': 'RS256', 'typ': 'JWT', 'kid': 'wks-T5EdzN8RzIcATVupl'})
@mock.patch('app.views.helpers.authentication.get_well_known_jwks',
            return_value='{"keys":[{"alg":"RS256","kty":"RSA","use":"sig","n":"kJ5itI5Rf5dE_UMmTCdi8NQbljgHWgU9615y_F8Hd9PWg_2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A_38h42fBwJjXfa3_KrvLXm5i-KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0-riHmgkVmIMpRY0fwnEz4wvjqoi-A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh-Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposw","e":"AQAB","kid":"wks-T5EdzN8RzIcATVupl","x5t":"Dk0ateKMS5FGXXIlJaStmqXxMxg","x5c":["MIIDDTCCAfWgAwIBAgIJKb8AZYZ1HwB9MA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJ5itI5Rf5dE/UMmTCdi8NQbljgHWgU9615y/F8Hd9PWg/2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A/38h42fBwJjXfa3/KrvLXm5i+KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0+riHmgkVmIMpRY0fwnEz4wvjqoi+A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh+Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSm8T/8EM4Bc6/U9XPE0o5TEOB3CDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAIlbQkA/BVjdE8QQs3jjKQbxVayemFa4usES4u76S90NkKAiP7v6ZuxBlVsHIDXbAxwPNa6h9yLvZU9EyELjnG0y3y/ja044b0mIyO9q7vvg97ttKCDvuNytaGuxj4TBYzEcCP/krll3DMWviVuwxTRoh/UNHS8tHqhEhFx9AKidc1k0S6+ltv5nOHZXn7BvX0tmILuaC45D4qHb+ZJDmguYGQBPtZhnx3NO7QfVF8Veu9uGqG2VqSzGMQaVLq90dUQKM3hpjffkpRKEtetFHYykLWpMyk2FKfN2yVpSl4JFlJxFsLNuBqYPk5PuHCxdhytayzXoqU644ZfFbnToOf4="]},{"alg":"RS256","kty":"RSA","use":"sig","n":"wIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1-j1USJVg-lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL_OxCFltHpNcFSOYXIhd-AacxQ6JLMZWYmXxAhI_k7CuDYulXH69hPz-qJFXcV-iFAMlzI-wYCm-5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN-g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQ","e":"AQAB","kid":"9nMOM4cMNY2BKpHNxpKf8","x5t":"O5k8zyePYH8wZofBVxBjgSDa1ZY","x5c":["MIIDDTCCAfWgAwIBAgIJPYHFYGfDrZ2xMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1+j1USJVg+lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL/OxCFltHpNcFSOYXIhd+AacxQ6JLMZWYmXxAhI/k7CuDYulXH69hPz+qJFXcV+iFAMlzI+wYCm+5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN+g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQBYXJM7mOlRCcps11/fY9dRgvLRjAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKQSDk1bXVlna1cSddh5Wut0v+RXWmffj409Pso15Yw6roVfp7bVSh1LyN3O0ETky5UuK3nHXxpkSA2Bs7wCwQ+aXC4vKYLf3NTzXzkEdJ/S6ZtZT0Gm8zL83GLYrIf6X9r1O73TTcS2/8KxxolPQB6+uj4N345+Gf6sHsjJd2lNJv485hLpn/DpeyzNM3r/IkyPMCuIv/Icitj4xXpkJ6p0kUZ4psLHoWbpFj/syjSTrgMeY+9oRXLYDZEr30tcXet8LXOr4EAV0Z79Z66A4FyUmkQJiESuJkd9VrMFJkmiDr4nds/5E6YZYk8m9n6TO9+ZHUn9UqtI71GfZdsqiU8="]}]}')
@mock.patch('app.views.helpers.authentication.get_token_auth_header', return_value='token')
def test_authenticate_invalid(_a, _b, _c, error, code, description, response_code):
    with pytest.raises(AuthError) as auth_error:
        with patch('jose.jwt.decode', side_effect=error):
            authenticate()

    assert auth_error.value.args[0].get('code') == code
    assert auth_error.value.args[0].get('description') == description
    assert auth_error.value.args[1] == response_code


@mock.patch('jose.jwt.get_unverified_header',
            return_value={'alg': 'RS256', 'typ': 'JWT', 'kid': 'aaa'})
@mock.patch('app.views.helpers.authentication.get_well_known_jwks',
            return_value='{"keys":[{"alg":"RS256","kty":"RSA","use":"sig","n":"kJ5itI5Rf5dE_UMmTCdi8NQbljgHWgU9615y_F8Hd9PWg_2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A_38h42fBwJjXfa3_KrvLXm5i-KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0-riHmgkVmIMpRY0fwnEz4wvjqoi-A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh-Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposw","e":"AQAB","kid":"wks-T5EdzN8RzIcATVupl","x5t":"Dk0ateKMS5FGXXIlJaStmqXxMxg","x5c":["MIIDDTCCAfWgAwIBAgIJKb8AZYZ1HwB9MA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJ5itI5Rf5dE/UMmTCdi8NQbljgHWgU9615y/F8Hd9PWg/2CxaoFl2ssHmf9Egh90osEUmnwwja1FYYYHj80HVMZRX5A/38h42fBwJjXfa3/KrvLXm5i+KtSBhhQUpSObNPLwT9btIsKIQOnpVE6ML7SNQxxh8gzQ1p3E6rtJUvspKunDCxxSHaG0K6pijq4ldt2jvdKGtG0+riHmgkVmIMpRY0fwnEz4wvjqoi+A5Gc1evpHEomxMbFtiH0UbVeFruVNVli81zEdnfHPkWJQno791SwTtHQmjmYFJkxuLQJzh+Wqsbq3FSMdzdWYvzWC6N2VjzPnbCpJCrLdKposwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSm8T/8EM4Bc6/U9XPE0o5TEOB3CDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAIlbQkA/BVjdE8QQs3jjKQbxVayemFa4usES4u76S90NkKAiP7v6ZuxBlVsHIDXbAxwPNa6h9yLvZU9EyELjnG0y3y/ja044b0mIyO9q7vvg97ttKCDvuNytaGuxj4TBYzEcCP/krll3DMWviVuwxTRoh/UNHS8tHqhEhFx9AKidc1k0S6+ltv5nOHZXn7BvX0tmILuaC45D4qHb+ZJDmguYGQBPtZhnx3NO7QfVF8Veu9uGqG2VqSzGMQaVLq90dUQKM3hpjffkpRKEtetFHYykLWpMyk2FKfN2yVpSl4JFlJxFsLNuBqYPk5PuHCxdhytayzXoqU644ZfFbnToOf4="]},{"alg":"RS256","kty":"RSA","use":"sig","n":"wIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1-j1USJVg-lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL_OxCFltHpNcFSOYXIhd-AacxQ6JLMZWYmXxAhI_k7CuDYulXH69hPz-qJFXcV-iFAMlzI-wYCm-5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN-g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQ","e":"AQAB","kid":"9nMOM4cMNY2BKpHNxpKf8","x5t":"O5k8zyePYH8wZofBVxBjgSDa1ZY","x5c":["MIIDDTCCAfWgAwIBAgIJPYHFYGfDrZ2xMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi12dzBlYWpycS51cy5hdXRoMC5jb20wHhcNMjEwMzEyMDg0MzMzWhcNMzQxMTE5MDg0MzMzWjAkMSIwIAYDVQQDExlkZXYtdncwZWFqcnEudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwIQNHOlsJJFpLCV5MoiQiUo45tXKwCGGN7j6Izf1+j1USJVg+lpjfqnMrNgQyQjOFpjerUgkCpxIhqoEhjkyeaNZiSrUdvsPIJvWLyL/OxCFltHpNcFSOYXIhd+AacxQ6JLMZWYmXxAhI/k7CuDYulXH69hPz+qJFXcV+iFAMlzI+wYCm+5ZgDcsrpkFsfAPC6ZeY5i3boYXQjvLyqxEL3w8vK2YKSmLWer2aaqHjMmnLAMnbGbN+g4aXqd0WcN0j2qyH8J1R9WRG0WZL8iOBeWY9gzf8ilCCM7DQZAReFMEPi5UiZWa0Swb1yNU99EOXoFS97KEt7ZrET6RJm3HYQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQBYXJM7mOlRCcps11/fY9dRgvLRjAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKQSDk1bXVlna1cSddh5Wut0v+RXWmffj409Pso15Yw6roVfp7bVSh1LyN3O0ETky5UuK3nHXxpkSA2Bs7wCwQ+aXC4vKYLf3NTzXzkEdJ/S6ZtZT0Gm8zL83GLYrIf6X9r1O73TTcS2/8KxxolPQB6+uj4N345+Gf6sHsjJd2lNJv485hLpn/DpeyzNM3r/IkyPMCuIv/Icitj4xXpkJ6p0kUZ4psLHoWbpFj/syjSTrgMeY+9oRXLYDZEr30tcXet8LXOr4EAV0Z79Z66A4FyUmkQJiESuJkd9VrMFJkmiDr4nds/5E6YZYk8m9n6TO9+ZHUn9UqtI71GfZdsqiU8="]}]}')
@mock.patch('app.views.helpers.authentication.get_token_auth_header', return_value='token')
def test_authenticate_invalid_no_key(_a, _b, _c):
    with pytest.raises(AuthError) as auth_error:
        authenticate()

    assert auth_error.value.args[0].get('code') == 'invalid_header'
    assert auth_error.value.args[0].get('description') == 'Unable to find appropriate key'
    assert auth_error.value.args[1] == 401
