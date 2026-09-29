#!/usr/bin/env python3
"""Script de despacho para enviar el avatar a una reunion de Google Meet.

Requisitos:
    pip install -r requirements.txt

Variables necesarias en .env:
    LIVEKIT_URL=wss://...
    LIVEKIT_API_KEY=API...
    LIVEKIT_API_SECRET=...

Uso:
    python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Clau --universidad TEC --sesion 01
"""

import argparse
import asyncio
import json
import os
import ssl
import sys
import uuid

import aiohttp
from dotenv import load_dotenv

load_dotenv()

# Sanitizar posibles comillas
for _k, _v in list(os.environ.items()):
    if _v and len(_v) >= 2 and ((_v[0] == '"' and _v[-1] == '"') or (_v[0] == "'" and _v[-1] == "'")):
        os.environ[_k] = _v[1:-1]

AGENT_NAME = "meet-bot"
VALID_AVATARS = ["Tony", "Clau", "Julius"]
VALID_UNIVERSITIES = ["UP", "TEC", "UNAM"]


def check_env() -> None:
    required = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        print("[ERROR] Faltan variables de entorno necesarias:")
        for var in missing:
            print(f"  - {var}")
        print("\nSolucion: copia el archivo de ejemplo y revisa sus valores:")
        print("  cp .env.example .env")
        sys.exit(1)


async def main() -> None:
    check_env()

    from livekit import api

    parser = argparse.ArgumentParser(
        description="Despachar avatar a una reunion de Google Meet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos de uso:
  python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Clau --universidad TEC --sesion 01
  python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Tony --universidad UP --sesion 02
  python avatar.py "https://meet.google.com/abc-defg-hij" --avatar Julius --universidad UNAM --sesion 03
""",
    )
    parser.add_argument("meeting_url", help="URL completa de la reunion de Google Meet")
    parser.add_argument(
        "--avatar",
        choices=VALID_AVATARS,
        default="Tony",
        help="Avatar a utilizar: Tony (hombre), Clau (mujer), Julius (hombre). Default: Tony",
    )
    parser.add_argument(
        "--universidad",
        choices=VALID_UNIVERSITIES,
        default="UP",
        help="Perfil y tono institucional: UP, TEC, UNAM. Default: UP",
    )
    parser.add_argument(
        "--sesion",
        default=None,
        help="Identificador de la sesion (ej. '01', '02'). Se incluye en el nombre de la minuta.",
    )
    parser.add_argument(
        "--bot-name",
        default=None,
        help="Nombre visible del participante en la llamada (default: nombre del avatar)",
    )
    parser.add_argument(
        "--no-chat",
        action="store_true",
        help="Desactivar la lectura de mensajes del chat de la llamada",
    )
    parser.add_argument(
        "--objective",
        default=None,
        help="Objetivo de la sesion para incluir en la minuta",
    )
    args = parser.parse_args()

    metadata = {
        "meeting_url": args.meeting_url,
        "avatar": args.avatar,
        "universidad": args.universidad,
        "bot_name": args.bot_name or args.avatar,
        "listen_to_meeting_chat": not args.no_chat,
    }
    if args.sesion:
        metadata["session_id"] = args.sesion
    if args.objective:
        metadata["objective"] = args.objective

    # Crear contexto SSL Inseguro (omite validación de certificados)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Crear sesión aiohttp sin verificación SSL para LiveKit API
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with api.LiveKitAPI(session=session) as lkapi:
            room_name = f"meet-bot-{uuid.uuid4().hex[:8]}"
            await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
            dispatch = await lkapi.agent_dispatch.create_dispatch(
                api.CreateAgentDispatchRequest(
                    agent_name=AGENT_NAME,
                    room=room_name,
                    metadata=json.dumps(metadata),
                )
            )
            print(f"\n[OK] Despachado exitosamente")
            print(f"  Avatar:      {args.avatar}")
            print(f"  Universidad: {args.universidad.upper()}")
            print(f"  URL:         {args.meeting_url}")
            if args.sesion:
                print(f"  Sesion ID:   {args.sesion}")
            print(f"  Room:        {room_name}")
            print(f"  Dispatch ID: {dispatch.id}")
            print("\nSiguiente paso: ve a Google Meet y admite al participante en la sala de espera.\n")


if __name__ == "__main__":
    asyncio.run(main())
