# TODOS

- [x] Unificar API
- [x] Como grabar reuniones en Linux ideal usar OBS Studio
- [x] Mover el API KEY a un depends de FastAPI
- [x] Permitir que la gente suba archivos y se guardarlo usando un StorageService
  - [x] LocalDirectoryService
  - [x] S3Service
- [x] Cuando se crea un QR se guarda usando el StorageService y tambien se descarga el archivo generado para el usuario
- [ ] Crear un tests de toda el API usando pytest y crear una carpeta aparte para los tests que se llame tests
- [x] Dividir scan_qr en 2 funciones, redirecionar y obtener informaccion geografica
- [x] Dividir el codigo en API, servicios y modelos
    - Servicio: Es un Wraper encima de la DB, nos permite hacer operaciones CRUD
      - Abstraer la interaccion con la DB, esto hace que si en un futuro queremos cambiar de DB, solo tenemos que cambiar el servicio
        - Ej: QRService signatures (Investigar que es un Service Layer y q es un signature)
          - ESTO ES UN EJEMPLO NO TIENE Q SER ASI
          - __init__(db: Session)
          - create_qr(data: QRCreate) -> QR
          - get_qr(short_url: str) -> QR
          - update_qr(short_url: str, data: QRUpdate) -> QR
          - delete_qr(short_url: str) -> None
- [x] Cambair geoip por una que no tenga limite de requests
  - [x] Mantener el codigo el anterior y añadir una funcion adicional
    - [x] Bueno comparar que diferencias hay entre las 2  cual es más precisa
- [ ] Crear servicio para manejo de archivos
    - [x] LocalDirectoryService
    - [x] S3Service
    - [ ] GCSService
- [ ] Editar un QR
  - [ ] Whatsapp www.whatsapp.com/send?phone=+{{NUMERO}}&text={{TEXTO_URL_ENCODEADO}}
    - [ ] Quiero cambiar el número o el texto pero mantener el mismo QR
    - QR [[[[[[[]]]]]]] -> url/scan/{{id}} -> redirige a www.whatsapp.com/send?phone=+{{NUMERO}}&text={{TEXTO_URL_ENCODEADO}}
      - En vez de apuntar a www.whatsapp.com/send?phone=+{{NUMERO}}&text={{TEXTO_URL_ENCODEADO}}
- [x] Añadir logo en la mitad del QR q se vea medio bonito (libreria PIL)
- [x] CLI tool para usarlo
  - [x] Comandos sencillos para ejecutar el API desde la terminal
  - [x] Comandos para crear QRs desde la terminal. Ej: python qr_tool.py create --url "https://example.com" --output "qrcode.png"
  - [x] Comandos para escanear QRs desde la terminal. Ej: python qr_tool.py scan --image "qrcode.png"

- ENTREGAR A CAMILO

- [ ] Cambiar Base de Datos por:
  - [ ] PostgresSQL
  - [ ] DynamoDB (AWS)
  - [ ] Dict in Memory (Para pruebas unitarias)
  - [ ] SQLite (Para pruebas unitarias)
- [ ] Deployear en AWS Lambda con API Gateway
  - [ ] Usar AWS SAM para desplegar en el repo que Camilo me va a compartir
- [ ] Testeamos en Vida real y vamos a crear QRs


La empresa se llama Pymtech

- OAuth usando nginx and oauth2_proxy (AWS)
  - Serve behing the documentation using Makedocs
