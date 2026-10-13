# Organizador de pastas

Script em Python que pega aquela pasta de Downloads lotada e separa tudo em subpastas: Imagens, Documentos, Planilhas, Vídeos, Áudios, Compactados, Instaladores e Outros.

- Por padrão só mostra o que faria, sem mexer em nada.
- Com `--executar` move os arquivos e salva um CSV com o que foi parar onde.
- Se já existir arquivo com o mesmo nome, renomeia pra `nome (1).ext` em vez de sobrescrever.
- Não precisa instalar nada, só Python 3.8+.

```bash
python organizar_arquivos.py ~/Downloads
python organizar_arquivos.py ~/Downloads --executar
```

Dá pra adaptar fácil: renomear fotos pela data, separar notas fiscais por mês, juntar PDFs etc.
