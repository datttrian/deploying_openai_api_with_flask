cp .env.example .env
source .env
poetry update
poetry install
poetry run flask db init
poetry run flask db migrate
poetry run flask db upgrade
npm install
npm run-script build
npm start
