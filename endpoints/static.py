from h11 import Request
from starlette.responses import HTMLResponse

token_page = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Token create</title>
</head>
<body>
<div style="text-align: center;">
    Created token: <span id="token"></span>
</div>
<script>
    // Get token from cookie
    const token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];

    if (token) {
        document.getElementById('token').innerText = token;
    }
</script>
</body>
</html>
"""


async def token(request: Request):
    """ Returns page, that shows the token """
    return HTMLResponse(token_page)
