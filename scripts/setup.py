import subprocess

CONFIG_FILE = "config.ini"
ENV_FILE = ".env"


def docker_compose_up():
    """
    Ejecuta docker compose build + up con el tag del proyecto.
    """
    # Leer el .env compilado
    env_vars = {}
    with open(ENV_FILE) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    project = env_vars.get("DEFAULT_PROJECT_NAME")

    print(f"🚀 Construyendo proyecto: {project}")

    subprocess.run(
        ["docker", "compose", "-p", f"{project}", "build", "--build-arg", "ENV=dev"],
        check=True,
    )
    subprocess.run(["docker", "compose", "-p", f"{project}", "up", "-d"], check=True)


def main():
    docker_compose_up()


if __name__ == "__main__":
    main()
