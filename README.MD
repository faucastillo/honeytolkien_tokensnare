# TokenSnare
Generador y servidor de honeytokens. Permite crear documentos con trackers e iniciar un servidor que registra los hits.

# Instalación y despliegue
Requisitos
- Docker y Docker Compose instalados.
- Git

### Pasos
1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/honeytolkien_tokensnare.git
cd honeytolkien_tokensnare
```
2. Configurar variables de entorno
```bash
cp .env.example .env
```
3. Preparar plantillas de binarios 

Para el HoneyToken binario se incluyen los templates de linux y windows por comodidad, 
pero se pueden regenerar con docker sin necesidad de instalar Go a partir del stub.go utilizando los comandos:
```bash
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp -e GOOS=windows -e GOARCH=amd64 golang:alpine go build -ldflags "-H=windowsgui -s -w" -o template_win.exe stub.go

docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp -e GOOS=linux -e GOARCH=amd64 golang:alpine go build -ldflags "-s -w" -o template_linux stub.go
```
4. Iniciar el servidor
```bash
docker compose up
```
Se puede agregar -d para que corra en segundo plano.

---

Recordar crear la carpeta honeyTokens con el usuario del equipo para permitir que el contenedor pueda escribir.
Si la crea el daemon de docker se crea como root.

---

Para detener el servidor, utilizar Ctrl+C o:
```
docker compose down
```

# Uso
1. Acceso al Dashboard
Abrir en el navegador
```bash
http://$SERVER:$PORT

Por defecto es:

http://localhost:5000
```
- Usuario por defecto: `admin` 
- Contraseña por defecto: `admin`

Es una herramienta para visualizar los tokens creados y las alertas generadas.

2. Generación de Honeytokens (CLI)

**Tipos implementados:**
- docx
- pdf
- xlsx
- epub
- qrcode
- binary
- Clonación de sitio web


**Sintaxis general:**
```bash
docker compose exec app python tokensnare_cli.py --type <TIPO> --output <NOMBRE_ARCHIVO> [OPCIONES]
```
***Argumentos Comunes:***

- server: URL del servidor (Por defecto http://127.0.0.1:5000).

- description: Nota interna para identificar el token en el dashboard.

- author: (Opcional) Metadatos de autor del archivo.

- title: (Opcional) Título del documento.

## Ejemplos
1. **Documento Word (.docx):**

```bash
docker-compose exec app python tokensnare_cli.py --type docx --title "Archivo confidencial" --content "Este es un archivo confidencial que no debería ser leído por personas no autorizadas" --output confidencial.docx --author "Elon Musk" --description "Archivo guardado en home/CarpetaUltraSecreta/"
```
2. **Documento PDF (.pdf):** Requiere visores que permitan conexiones, como Adobe Acrobat Reader.

```bash
docker compose exec app python tokensnare_cli.py --type pdf --title "Informe confidencial" --content "Este es un informe confidencial de la empresa." --description "Este es un honeytoken PDF de ejemplo" --author "Ricardo Bochini" --output informe.pdf
```

# Modo "manual"
## Server
` python3 tokensnare_server.py --host $ip --port 5000 `

## Cli

### Ejemplo Word
`python3 tokensnare_cli.py --type docx --output prueba_docx.docx --server $ip`