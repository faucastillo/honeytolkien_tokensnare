# TokenSnare

Generador y servidor de honeytokens. Permite crear documentos con trackers e iniciar un servidor que registra los hits.

## Requisitos
- Docker
- ...

## Ejecutar la aplicación
Se utiliza docker compose para ejecutar a la vez el servidor y poder crear honeytokens vía CLI.
```bash
docker compose up
```
Se puede agregar -d para correr en segundo plano.

Recordar crear la carpeta honeyTokens con el usuario del equipo para permitir que el contenedor pueda escribir.
Si la crea el daemon de docker se crea como root.

Una vez que está corriendo el servidor, se puede ejecutar la herramienta CLI de generación de honeytokens:
```bash
docker compose exec app python tokensnare_cli.py --type pdf --output test.pdf --description test
```

Para detener el servidor, utilizar Ctrl+C o:
```bash
docker compose down
```