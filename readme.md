# Base64 api
A basic api to convert any given string to a base64 string. 

## Usage

The api takes only one request parameter:
- `input`

Example request:
```json
{
    "input": "This is a normal string"
}
```

Response:
```json
{
    "status": 200,
    "result": "VGhpcyBpcyBhIG5vcm1hbCBzdHJpbmc="
}
```

## Security

The api is protected by a x-api-key header. The key can be set in a .env file or docker environment variable using `KEY` as the key. 
