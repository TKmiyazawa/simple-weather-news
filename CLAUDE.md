# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Serverless weather news system (サーバーレス会員制天気ニュースシステム) - a PoC for 5 Japanese cities (札幌, 東京, 名古屋, 大阪, 博多) with Cognito authentication.

**Tech Stack**: Python 3.12 Lambda, API Gateway, DynamoDB, Cognito | React 18, Vite, Amplify UI | AWS SAM (ap-northeast-1)

## Commands

```bash
# Install all dependencies
make install

# Run tests
make test                                      # All tests (backend + frontend)
python -m pytest tests/ -v                     # Backend only
python -m pytest tests/test_weather_handler.py -v  # Single file
python -m pytest tests/ -v -m unit             # By marker (unit|integration|property)
python -m pytest tests/ -v -k "test_health"    # By test name pattern
python -m pytest tests/ -v --cov=src --cov-report=html  # With coverage

# CSV ingest tests (separate module)
cd csv_ingest && python3 test_app.py           # Unit tests
cd csv_ingest && python3 integration_test.py   # Integration tests

# Local development
sam local start-api --port 3001                # Backend API
cd simple-weather-frontend && npm run dev      # Frontend dev server

# Deployment
make deploy STAGE=dev REGION=ap-northeast-1    # Dev environment
make prod-deploy                               # Production
make validate                                  # Validate SAM template
make status && make outputs                    # Check deployment
make logs                                      # Lambda logs (tail)
```

## Architecture

### Request Flow
CloudFront → S3 (React SPA) or API Gateway → Lambda (`weather_handler.py`) → DynamoDB

### Backend (`src/`)
- `weather_handler.py` - Lambda handler with API routing (entry point)
- `weather_service.py` - Business logic for weather operations
- `auth_middleware.py` - `@require_auth` decorator for protected endpoints
- `database.py` - DynamoDB CRUD operations
- `auth_service.py`, `models.py`, `exceptions.py`

### API Endpoints
| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /health` | No | Health check |
| `GET /weather` | Yes | All 5 cities weather |
| `POST /weather/generate` | Yes | Generate random data |
| `GET /weather/forecast` | Yes | Weather forecast |
| `GET /weather/statistics` | Yes | Statistics |
| `GET /weather/types` | No | Weather type list |

### CSV Ingestion (`csv_ingest/`)
S3-triggered Lambda for CSV import. Format (no header):
```
CityId,CityName,WeatherId,WeatherName,RainfallProbability
1,札幌,1,晴れ,10
```

### DynamoDB Schema
- Key: `CityId` (Number, HASH) + `timestamp` (String, RANGE)
- GSI: `timestamp-index`
- City IDs: 1=札幌, 13=東京, 23=名古屋, 27=大阪, 40=博多
- TTL: `ttl` attribute

### Frontend (`simple-weather-frontend/`)
React + Amplify Authenticator. Configure `src/config.js` (copy from `config.js.example`) with Cognito and API Gateway values from `make outputs`.

## Test Markers
- `unit` - Unit tests
- `integration` - Integration tests
- `property` - Property-based tests (Hypothesis)

## Code Patterns

**Authentication decorator**:
```python
from auth_middleware import require_auth

@require_auth
def handler(event, context):
    user = event['requestContext']['authorizer']['claims']
```

**Custom exceptions**: Use `AuthenticationError`, `WeatherDataError` from `exceptions.py`
