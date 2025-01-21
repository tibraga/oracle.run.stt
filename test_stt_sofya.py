"""STT Sofya Test"""

import json
import time
import sys
import pandas as pd

import requests
import jiwer as jw
import websocket as ws
from utils import load_resource

def get_res(websocket):
    """try read with timout"""
    try:
        result = json.loads(websocket.recv())
        print_result(result)
        return result
    except ws.WebSocketTimeoutException:
        return {}


def print_result(result: dict):
    """print result and execution time"""
    # if bool(result["is_partial"]) is False:
    print(result["is_partial"], round(result["time"], 2), result["data"]["text"])


def test_send_chunks(host_ws:str, audio_path: str, language: str = "portuguese", chunk_size=4096):
    """
    Envia os chunks de áudio para o serviço STT.

    :param audio_path: Caminho do arquivo de áudio (obrigatório).
    :param language: Idioma da transcrição (default = "portuguese").
    :param chunk_size: Tamanho do chunk em bytes (default = 4096).
    """
    # Monta a URL com o idioma apropriado
    url = f"{host_ws}?transcription_language={language}"
    
    # Cria conexao websocket
    websocket = ws.create_connection(url)
    websocket.settimeout(5)

    # Carrega o recurso de áudio usando a função utilitária
    # Aqui você ajusta se a sua função `ut.load_resource` precisa de um path completo
    # ou algum identificador sem extensões etc.
    resource = load_resource(audio_path)

    # Divide o áudio em chunks
    audio_bytes = resource["audio"]
    chunks = [
        audio_bytes[i : i + chunk_size] for i in range(0, len(audio_bytes), chunk_size)
    ]

    df_result = pd.DataFrame(columns=["is_partial", "latency", "result"])
    # for chunk in chunks:
    #     websocket.send_bytes(chunk)
    #     res = get_res(websocket)
    #     if res:
    #         df_result.loc[len(df_result)] = [
    #             res["is_partial"],
    #             round(res["time"], 2),
    #             res["data"]["text"],
    #         ]
    websocket.send_bytes(audio_bytes)
    res = get_res(websocket)
    if res:
        df_result.loc[len(df_result)] = [
            res["is_partial"],
            round(res["time"], 2),
            res["data"]["text"],
        ]

    # Tenta receber respostas finais por algumas tentativas
    attempts = 0
    while attempts < 3:
        res = get_res(websocket)
        if res:
            attempts = 0
            df_result.loc[len(df_result)] = [
                res["is_partial"],
                round(res["time"], 2),
                res["data"]["text"],
            ]
        else:
            attempts += 1
            time.sleep(5000)

    pd.set_option("max_colwidth", 800)
    print("Latency Stats:\n", df_result["latency"].describe())

    # Fecha o websocket
    websocket.close()


if __name__ == "__main__":
    # Caso rode diretamente: python stt_test.py /caminho/audio.wav [language]
    if len(sys.argv) < 3:
        print("Uso: python stt_test.py <host_ws> <audio_path> [idioma]")
        sys.exit(1)

    # Argumento obrigatório: caminho do áudio
    host_ws = sys.argv[1]

    # Argumento obrigatório: caminho do áudio
    audio_path = sys.argv[2]

    # Argumento opcional: idioma (com default = portuguese)
    if len(sys.argv) > 3:
        language = sys.argv[3]
    else:
        language = "portuguese"

    print("Starting STT Sofya Test")
    test_send_chunks(host_ws=host_ws, audio_path=audio_path, language=language)
    print("STT Sofya Test Completed")
