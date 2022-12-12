# Backend

![Gitlab pipeline status (self-managed)](https://img.shields.io/gitlab/pipeline-status/indicators-parser-saas/backend?branch=master&gitlab_url=https%3A%2F%2Fgit.miem.hse.ru)
![Gitlab code coverage (self-managed)](https://img.shields.io/gitlab/pipeline-coverage/indicators-parser-saas/backend?branch=master&gitlab_url=https%3A%2F%2Fgit.miem.hse.ru)
![Lines of code](https://tokei.rs/b1/git.miem.hse.ru/indicators-parser-saas/backend?category=code)

Monolithic backend of IoC scraper service

## Deploy

### Native deployment

1. Install python 3.10
2. Clone repository
    ```bash
    git clone https://git.miem.hse.ru/indicators-parser-saas/backend.git
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
4. Set enviroment variables in .env file
5. Run development server
    ```bash
    python main.py
    ```

### Docker deployment

1. Install docker
2. Save enviroment variables in .env file
3. Run docker image
    ```bash
    docker run -d --env-file .env -p 8000:8000 --name backend registry.miem.hse.ru/indicators-parser-saas/backend
    ```

## Settings

|        **Name**        |                                                   **Description**                                                   | **Is required?** |
|:----------------------:|:-------------------------------------------------------------------------------------------------------------------:|:----------------:|
|        `DB_URI`        |                              Database [URL](https://tortoise.github.io/databases.html)                              |         ✅        |
|   `GITHUB_CLIENT_ID`   |   [GitHub OAuth](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps) client id   |         ✅        |
| `GITHUB_CLIENT_SECRET` | [GitHub OAuth](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps) client secret |         ✅        |
|     `JWK_KEY_FILE`     |                        RSA Private and Public key in Json Web Key format (key.jwk by default)                       |                  |
|     `S3_SECRET_KEY`    |                                     AWS S3 or S3 like storage static key secret                                     |         ✅        |
|     `S3_ACCESS_KEY`    |                                     AWS S3 or S3 like storage static access key                                     |         ✅        |
|    `S3_REGION_NAME`    |                                        AWS S3 or S3 like storage region name                                        |         ✅        |
|    `S3_ENDPOINT_URL`   |                                        AWS S3 or S3 like storage endpoint URL                                       |         ✅        |
|   `S3_REPORTS_FOLDER`  |                                     AWS S3 or S3 like storage reports base path                                     |                  |
|      `S3_BASE_URL`     |                                       Base URL for generating not signed URLs                                       |         ✅        |

## Documentation

`//TODO: Add documentation here`
