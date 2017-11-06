# python-dciauth

DCI authentication module used by dci-control-server and python-dciclient

## Summary of signing steps

To create a signed request, complete the following:

 * Task 1: Hash payload you want to send

 * Task 2: Create a string to sign

   Create a string to sign with the request and extra information such as the request date, and the payload (hash) of the request.

 * Task 3: Calculate the signature for DCI

   Derive a signing key by performing a succession of keyed hash operations (HMAC operations) on the string to sign, with your API secret.

 * Task 4: Add the Signing Information to the Request

   After you calculate the signature, add it to an HTTP header or to the query string of the request.

## Summary of the validation steps

 * Task 1: Hash payload you received

 * Task 2: Create a string to sign

   Create a string to sign with the request and extra information such as the request date **header**, and the payload (hash) of the request.

 * Task 3: Calculate the signature for DCI

   Derive a signing key by performing a succession of keyed hash operations (HMAC operations) on the string to sign, with user's API secret.

 * Task 4: Compare signature calculated with signature send

   After you calculate the signature, compare it to an HTTP header.

 * Task 5: Reject any request older than 5 minutes

## Signing example:

```python
    from dciauth import signature

    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "GET"
    content_type = 'application/json'
    url = "/api/v1/jobs"
    query_string = "limit=100&offset=1"
    payload = {}
    headers = signature.generate_headers_with_secret(
        secret,
        method,
        content_type,
        url,
        query_string,
        payload)

    # headers == {
    #     'Authorization': 'DCI-HMAC-SHA256 811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b',
    #     'Content-Type: 'application/json',
    #     'DCI-Datetime': '20171103T162727Z'
    # }
```

## Validation example

```python
    from dciauth import signature

    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    method = "GET"
    headers = {
        'Authorization': 'DCI-HMAC-SHA256 811f7ceb089872cd264fc5859cffcd6ddfbe8ce851f0743199ad4c96470c6b6b',
        'DCI-Datetime': '20171103T162727Z',
        'Content-type': 'application/json'
    }
    url = "/api/v1/jobs"
    query_string = "limit=100&offset=1"
    payload = {}
    expected_signature = signature.calculate_signature(
        secret,
        method,
        headers,
        url,
        query_string,
        payload)
    dci_signature = signature.get_signature_from_headers(headers)

    if signature.equals(expected_signature, dci_signature):
        raise Exception("Authentication failed: signature invalid")

    if signature.is_expired(headers):
        raise Exception("Authentication failed: signature expired")

```

## Validation example with flask request

```python
    from dciauth import signature
    from flask import request

    secret = "Y4efRHLzw2bC2deAZNZvxeeVvI46Cx8XaLYm47Dc019S6bHKejSBVJiGAfHbZLIN"
    headers = request.headers
    expected_signature = signature.calculate_signature(
        secret,
        method = request.method,
        headers = headers,
        url = request.path,
        query_string = request.query_string.decode('utf-8'),
        payload = request.get_json(silent=True)
    )
    dci_signature = signature.get_signature_from_headers(headers)

    if signature.equals(expected_signature, dci_signature):
        raise Exception("Authentication failed: signature invalid")

    if signature.is_expired(headers):
        raise Exception("Authentication failed: signature expired")

```

## Implementation details

Along each request, the client must add the three following HTTP headers:

 * `Authorization`
 * `Content-Type`
 * `DCI-Datetime`

They are build as following

### Content-Type

`Content-Type` (e.g.: `application/json`) of the request

### DCI-Datetime

`DCI-Datetime` is the current client timestamp in UTC timezone with the following format: `%Y%m%dT%H%M%SZ` (e.g.: `20170612T142917Z`)

### Authorization

The signature header `Authorization:<algorithm> <signature>` is obtained with:

 * `<algorithm>`: only `DCI-HMAC-SHA256`
 * `<signature>`: `hexdigest( HMAC-SHA256( <api secret>, <string_to_sign>.encode('utf-8') ) )`
 * `<string_to_sign>`:

        <HTTP Verb> + "\n"
        <Content-Type> + "\n"
        <timestamp> + "\n"
        <url> + "\n"
        <query_string> + "\n"
        <payload hash>

     * `<HTTP Verb>`: the HTTP method used in uppercase
     * `<Content-Type>`: Usually `application/json` for API calls
     * `<timestamp>`: as previously, the client timestamp in UTC timezone with the following format: `%Y%m%dT%H%M%SZ`
     * `<url>`: the resource path, without query string
     * `<query_string>`: the parameter passed when querying (the part after the `?` in the full URL)
     * `<payload hash>`: `hexdigest( SHA256( payload ) )`

See `tests/test_signature.py` for some detailed examples

## License

Apache 2.0


## Author Information

Distributed-CI Team  <distributed-ci@redhat.com>
