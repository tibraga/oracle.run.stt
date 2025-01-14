# STT Sofya Test
Este repositório contém um script Python que realiza testes de Speech-To-Text (STT), enviando áudio em chunks para um servidor WebSocket que processa a transcrição.

## Visão Geral
O script stt_test.py se conecta a um endpoint WebSocket definido pelo usuário, envia o áudio em pedaços (chunks), monitora a latência e exibe o resultado parcial e final das transcrições. É possível também especificar o idioma de transcrição (por padrão, "portuguese").


## Requisitos
- Python 3.11+
- Bibliotecas listadas no arquivo requirements.txt
- Um serviço de STT rodando em algum endpoint WebSocket para receber o áudio e retornar a transcrição.
- Um arquivo de áudio adequado, no formato com taxa de amostragem 16kHz.

## Execução
Para executar o script, utilize:

```bash
python test_stt_sofya.py <host_ws> <audio_path> [idioma]
```
Onde:

- host_ws (Obrigatório).
Endereço do serviço WebSocket que realizará a transcrição.
Exemplo: ws://10.11.90.11:8000/

- audio_path (Obrigatório).
Caminho do arquivo de áudio ou identificador necessário para a função load_resource.

- idioma (Opcional).
O idioma de transcrição (ex.: portuguese, english, etc.). No final desse documento mostra os idiomas suportados. Caso não seja informado, será considerado o valor padrão "portuguese".

## Exemplo
```bash
# Rodando o script com idioma padrão (portuguese)
python stt_test.py ws://10.11.90.11:8000/ /home/user/audios/exemplo.wav

# Rodando o script especificando o idioma
python stt_test.py ws://10.11.90.11:8000/ /home/user/audios/exemplo.wav english
```

## O que o script faz?
- Cria uma conexão WebSocket com o servidor STT usando o host_ws + parâmetro de idioma.
- Carrega o arquivo de áudio em bytes através da função load_resource(audio_path).
- Divide o áudio em chunks (blocos) de 4096 bytes (valor padrão chunk_size), enviando cada chunk ao servidor.
- Recebe as respostas parciais e finais do servidor, registrando:
  - se é parcial (is_partial)
  - a latência (time)
  - o texto transcrito (data["text"])
- Exibe estatísticas de latência (média, desvio padrão etc.) no final do processo.
- Encerra a conexão WebSocket.

## Idiomas suportados
- afrikaans
- amharic
- arabic
- assamese
- azerbaijani
- bashkir
- belarusian
- bulgarian
- bengali
- tibetan
- breton
- bosnian
- catalan
- czech
- welsh
- danish
- german
- greek
- english
- spanish
- estonian
- basque
- persian
- finnish
- faroese
- french
- galician
- gujarati
- hausa
- hawaiian
- hebrew
- hindi
- croatian
- haitian
- hungarian
- armenian
- indonesian
- icelandic
- italian
- japanese
- javanese
- georgian
- kazakh
- khmer
- kannada
- korean
- latin
- luxembourgish
- lingala
- lao
- lithuanian
- latvian
- malagasy
- maori
- macedonian
- malayalam
- mongolian
- marathi
- malay
- maltese
- burmese
- nepali
- dutch
- norwegian nynorsk
- norwegian
- occitan
- punjabi
- polish
- pashto
- portuguese
- romanian
- russian
- sanskrit
- sindhi
- sinhalese
- slovak
- slovenian
- shona
- somali
- albanian
- serbian
- sundanese
- swedish
- swahili
- tamil
- telugu
- tajik
- thai
- turkmen
- tagalog
- turkish
- tatar
- ukrainian
- urdu
- uzbek
- vietnamese
- yiddish
- yoruba
- chinese
- cantonese
- multi
