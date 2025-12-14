# サーバーレス天気ニュースシステム Makefile

.PHONY: install test deploy clean validate outputs logs status prod-deploy frontend-build frontend-deploy

# デフォルト設定
STAGE ?= dev
REGION ?= ap-northeast-1
STACK_NAME ?= simple-weather-news-$(STAGE)

# 依存関係インストール
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd simple-weather-frontend && npm install

# テスト実行
test:
	@echo "Running backend tests..."
	python -m pytest tests/ -v
	@echo "Running frontend tests..."
	cd simple-weather-frontend && npm test -- --run

test-backend:
	python -m pytest tests/ -v

test-frontend:
	cd simple-weather-frontend && npm test -- --run

test-unit:
	python -m pytest tests/ -v -m unit

test-integration:
	python -m pytest tests/ -v -m integration

test-property:
	python -m pytest tests/ -v -m property

test-coverage:
	python -m pytest tests/ -v --cov=src --cov-report=html

# SAMテンプレート検証
validate:
	sam validate --template template.yaml

# ビルド
build:
	sam build --template template.yaml

# デプロイ（開発環境）
deploy: validate build
	sam deploy \
		--stack-name $(STACK_NAME) \
		--parameter-overrides Stage=$(STAGE) \
		--capabilities CAPABILITY_IAM \
		--region $(REGION) \
		--resolve-s3 \
		--no-confirm-changeset

# 本番環境デプロイ
prod-deploy:
	$(MAKE) deploy STAGE=prod

# スタック出力値確認
outputs:
	aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[0].Outputs' \
		--output table \
		--region $(REGION)

# デプロイ状態確認
status:
	aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[0].StackStatus' \
		--output text \
		--region $(REGION)

# Lambdaログ確認
logs:
	sam logs \
		--stack-name $(STACK_NAME) \
		--name WeatherFunction \
		--tail \
		--region $(REGION)

# フロントエンドビルド
frontend-build:
	cd simple-weather-frontend && npm run build

# フロントエンドデプロイ
frontend-deploy: frontend-build
	@BUCKET=$$(aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
		--output text \
		--region $(REGION)); \
	aws s3 sync simple-weather-frontend/dist s3://$$BUCKET --delete --region $(REGION)

# ローカル開発サーバー起動
local-api:
	sam local start-api --port 3001

local-frontend:
	cd simple-weather-frontend && npm run dev

# クリーンアップ
clean:
	rm -rf .aws-sam
	rm -rf simple-weather-frontend/dist
	rm -rf simple-weather-frontend/node_modules
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

# スタック削除（要注意）
destroy:
	@echo "WARNING: This will delete the stack $(STACK_NAME)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	aws cloudformation delete-stack \
		--stack-name $(STACK_NAME) \
		--region $(REGION)

# ヘルプ
help:
	@echo "Available targets:"
	@echo "  install        - Install all dependencies"
	@echo "  test           - Run all tests"
	@echo "  test-backend   - Run backend tests only"
	@echo "  test-frontend  - Run frontend tests only"
	@echo "  validate       - Validate SAM template"
	@echo "  build          - Build SAM application"
	@echo "  deploy         - Deploy to AWS (dev)"
	@echo "  prod-deploy    - Deploy to AWS (prod)"
	@echo "  outputs        - Show stack outputs"
	@echo "  status         - Show stack status"
	@echo "  logs           - Tail Lambda logs"
	@echo "  frontend-build - Build frontend"
	@echo "  frontend-deploy- Deploy frontend to S3"
	@echo "  local-api      - Start local API server"
	@echo "  local-frontend - Start frontend dev server"
	@echo "  clean          - Clean build artifacts"
	@echo "  destroy        - Delete stack (DANGEROUS)"
