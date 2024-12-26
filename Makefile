up:
	@docker compose -f ./srcs/docker-compose.yml up --build || true
	@echo "Up"
stop:
	@docker compose -f ./srcs/docker-compose.yml stop > /dev/null 2>&1 || true
	@echo "Stopped"
start:
	@docker compose -f ./srcs/docker-compose.yml start > /dev/null 2>&1 || true
	@echo "Started"
restart:
	@docker compose -f ./srcs/docker-compose.yml restart > /dev/null 2>&1 || true
	@echo "Restarted"
down:
	@docker compose -f ./srcs/docker-compose.yml down > /dev/null 2>&1 || true
	@echo "Down"
clean: down
	@sudo rm -rf ./srcs/auth_db/data > /dev/null 2>&1 || true
	@sudo rm -rf ./srcs/prof_db/data > /dev/null 2>&1 || true
	@sudo rm -rf srcs/auth_db/data \
		srcs/prof_db/data \
		srcs/profile/srcs/static \
		srcs/profile/srcs/avatars/uploads\
		srcs/profile/srcs/api/__pycache__ \
		srcs/profile/srcs/api/migrations \
		srcs/profile/srcs/user_profile/__pycache__ \
		srcs/authentication/srcs/static \
		srcs/authentication/srcs/api/__pycache__ \
		srcs/authentication/srcs/api/migrations \
		srcs/authentication/srcs/authentication/__pycache__ > /dev/null 2>&1 || true
	@docker volume rm $$(docker volume ls -q) > /dev/null 2>&1 || true
	@docker system prune -af > /dev/null 2>&1 || true
	@echo "Cleaned"