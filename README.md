# Cliente de Despacho — Avatar para Google Meet

Herramienta ligera para enviar un avatar de voz con contexto institucional a reuniones de Google Meet.

El procesamiento de audio, LLM y generacion de video se ejecuta en un servidor central en la nube. Este cliente solo envia la orden de despacho a la llamada.

---

## Requisitos previos

- Python 3.10 o superior instalado.
- Conexion a internet.

---

## Instalacion inicial (una sola vez)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/jtmancilla/google-meet-avatar-universidades.git
   cd google-meet-avatar-universidades
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   *(En Mac o Linux con varias versiones de Python, usar `pip3 install -r requirements.txt`)*.

3. Crear el archivo `.env`:
   ```bash
   cp .env.example .env
   ```
   *(El archivo `.env.example` ya contiene las credenciales preconfiguradas para conectarse al servidor central).*

---

## Uso

Para enviar un avatar a una llamada, ejecuta el script pasando el enlace de Google Meet:

```bash
python avatar.py "https://meet.google.com/xxx-xxxx-xxx" --avatar Clau --universidad TEC --sesion 01
```
*(En Mac o Linux, si `python` no esta enlazado, usar `python3 avatar.py ...`)*.

---

## Opciones disponibles

| Parametro | Opciones | Default | Descripcion |
|---|---|---|---|
| `meeting_url` | URL de Meet | Requerido | Enlace completo de la llamada |
| `--avatar` | `Tony`, `Clau`, `Julius` | `Tony` | `Tony` (hombre), `Clau` (mujer), `Julius` (hombre) |
| `--universidad` | `UP`, `TEC`, `UNAM` | `UP` | Tono y contexto: Universidad Panamericana (`UP`), Tecnologico de Monterrey (`TEC`), UNAM (`UNAM`) |
| `--sesion` | Texto (ej. `01`, `02`) | Opcional | Numero de sesion. Se incluye en el encabezado de las minutas generadas. |
| `--bot-name` | Texto | Nombre de avatar | Sobreescribe el nombre visible del participante en Google Meet. |
| `--no-chat` | Flag | Desactivado | Desactiva que el avatar lea mensajes enviados en el chat de Meet. |

---

## Ejemplos rapidos

### Clau en el Tecnologico de Monterrey
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Clau --universidad TEC --sesion 01
```

### Tony en la Universidad Panamericana
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Tony --universidad UP --sesion 02
```

### Julius en la UNAM
```bash
python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Julius --universidad UNAM --sesion 03
```

---

## Como interactuar con el avatar en la reunion

1. **Admitir al participante**:
   El bot aparecera en la sala de espera de Google Meet. Un participante humano debe admitirlo.

2. **Entrada en silencio**:
   El bot entra en silencio para no interrumpir la sesion.

3. **Modo wake-word**:
   Solo responde cuando se le llama por su nombre.
   - Para llamarlo: *"Hola Clau"*, *"Oye Tony"*, *"Julius, ¿que opinas de este tema?"*.
   - Frases de cierre: *"Gracias, eso es todo"* o *"Ya puedes irte"* lo regresan a silencio.

4. **Minuta o resumen de la sesion**:
   Si le dices *"Oye Clau, genera la nota de la sesion"*, resumira las acciones, acuerdos y pendientes acordados en la reunion.

5. **Terminar la sesion**:
   Para retirarlo de la llamada, simplemente expulsalo de la reunion desde el panel de participantes de Google Meet.
