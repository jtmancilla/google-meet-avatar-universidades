# Cliente de Despacho — Avatar para Google Meet

Herramienta ligera para enviar un avatar de voz con contexto institucional a reuniones de Google Meet.

El procesamiento de audio, LLM y generacion de video se ejecuta en un servidor central en la nube. Este cliente solo envia la orden de despacho a la llamada.

---

## Requisitos previos

- Python 3.10 o superior instalado.
- Conexion a internet.

---

## Instalacion y configuracion (una sola vez)

### 1. Clonar el repositorio
Abre tu terminal y clona la carpeta del proyecto:
```bash
git clone https://github.com/jtmancilla/google-meet-avatar-universidades.git
cd google-meet-avatar-universidades
```

### 2. Crear y activar un entorno virtual (Recomendado)
El entorno virtual aísla las librerías del proyecto para evitar conflictos con el sistema:

- **En macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **En Windows (PowerShell / CMD)**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

*(Notarás que tu terminal muestra el prefijo `(.venv)` indicando que el entorno está activo).*

### 3. Instalar dependencias
Dentro del entorno virtual activo, instala las dos librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Crear el archivo de configuracion `.env`
Genera tu archivo de credenciales a partir de la plantilla:
```bash
cp .env.example .env
```
*(El archivo `.env.example` ya contiene las credenciales de conexion al servidor central).*

---

## Uso diario

Cada vez que vayas a despachar un avatar:

1. Entra a la carpeta del proyecto:
   ```bash
   cd google-meet-avatar-universidades
   ```

2. Activa tu entorno virtual:
   - En macOS / Linux: `source .venv/bin/activate`
   - En Windows: `.venv\Scripts\activate`

3. Ejecuta el comando pasando el link de tu reunion de Google Meet.

---

## Ejemplos oficiales

### 1. Clau — Universidad Panamericana (UP)
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Clau --universidad UP --sesion 01
```

### 2. Ricardo — Universidad Nacional Autonoma de Mexico (UNAM)
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Ricardo --universidad UNAM --sesion 01
```

### 3. Tony — Tecnologico de Monterrey (TEC)
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Tony --universidad TEC --sesion 01
```

---

## Parametros disponibles

| Parametro | Opciones | Descripcion |
|---|---|---|
| `meeting_url` | URL de Google Meet | Requerido. Enlace completo de la reunion. |
| `--avatar` | `Clau`, `Ricardo`, `Tony` | Voz e imagen: `Clau` (mujer), `Ricardo` (hombre), `Tony` (hombre). |
| `--universidad` | `UP`, `UNAM`, `TEC` | Tono y contexto: Universidad Panamericana (`UP`), UNAM (`UNAM`), Tec de Monterrey (`TEC`). |
| `--sesion` | Texto (ej. `01`, `02`) | Opcional. Identificador de sesion para el encabezado de las notas. |
| `--bot-name` | Texto | Opcional. Sobreescribe el nombre visible en Google Meet si deseas uno distinto. |
| `--no-chat` | Flag | Opcional. Desactiva la lectura de mensajes del chat de la llamada. |

---

## Como interactuar con el avatar en la reunion

1. **Admitir al participante**:
   El avatar aparecera en la sala de espera de Google Meet pidiendo entrar. Un participante humano debe admitirlo.

2. **Entrada en silencio**:
   El bot entra en silencio absoluto para no interrumpir el inicio de la sesion.

3. **Modo wake-word (activacion por voz)**:
   Solo habla cuando se le llama directamente por su nombre:
   - Para hablar con Clau: *"Hola Clau, ¿nos escuchas?"* o *"Oye Clau, ¿que opinas de este punto?"*.
   - Para hablar con Ricardo: *"Hola Ricardo"* o *"Oye Ricardo, danos una introduccion"*.
   - Para hablar con Tony: *"Hola Tony, adelante con tu comentario"*.

4. **Regresar a silencio**:
   Frases como *"Gracias, eso era todo"* o *"Ya puedes irte"* lo regresan a silencio inmediatamente.

5. **Minuta de la sesion**:
   Si le dices *"Oye [Nombre], genera la nota de la sesion"*, guardara un documento estructurado con los acuerdos, acciones y pendientes tratados en la reunion.

6. **Terminar la sesion**:
   Para retirarlo, simplemente expulsalo de la llamada desde el panel de participantes de Google Meet. Al salir de la llamada se liberan los recursos y se detiene el servicio en el servidor.
