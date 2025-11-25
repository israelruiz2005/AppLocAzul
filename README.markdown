# Documentação do Script appLocAzul-v2.py

## Descrição
O script `appLocAzul-v2.py` é uma ferramenta desenvolvida para processar arquivos de texto em uma pasta específica, realizando modificações em linhas que contenham informações relacionadas à companhia aérea "AD" (Azul Linhas Aéreas). O script verifica arquivos na pasta de origem, realiza alterações específicas em linhas que atendem a determinados critérios, move os arquivos processados para uma pasta de destino e registra todas as ações em um arquivo de log.

## Funcionalidades
- **Leitura de Arquivos**: Lê arquivos de texto na pasta de origem (`\\REGENTEAPP\Senior\Regente\GDS\AGUARDANDO`) utilizando diferentes codificações (`utf-8`, `latin1`, `cp1252`) para garantir compatibilidade.
- **Verificação de Companhia Aérea**: Identifica arquivos que contêm a linha `A-CIA AEREA;AD` para processar apenas arquivos relevantes.
- **Modificação de Conteúdo**: Substitui códigos específicos (`AD 5770`, `AD 9030`, `T-K577-`, `T-#0413-`, `T-K903-`) pelo código `AD 4130` em linhas correspondentes.
- **Gerenciamento de Arquivos**: Move os arquivos processados para a pasta de destino (`\\REGENTEAPP\Senior\Regente\GDS`) e remove os arquivos originais após o processamento.
- **Registro de Log**: Gera um arquivo de log (`processing_log.txt`) na pasta de destino, contendo detalhes de cada operação, incluindo erros, modificações e movimentações de arquivos.

## Requisitos
- **Python 3**: O script deve ser executado utilizando Python 3, pois foi projetado e testado com esta versão.
- **Sistema Operacional**: O script é executado em um servidor com **Windows Server 2012 R2**. Certifique-se de que o ambiente possui as permissões necessárias para acessar as pastas de origem e destino.
- **Acesso às Pastas**: O servidor deve ter acesso às pastas de rede especificadas (`\\REGENTEAPP\Senior\Regente\GDS\AGUARDANDO` e `\\REGENTEAPP\Senior\Regente\GDS`).
- **Executável**: Um executável foi gerado utilizando o **PyInstaller** para facilitar a execução no servidor sem a necessidade de um ambiente Python instalado.
- **Agendamento**: O executável foi configurado em uma rotina no **Agendador de Tarefas do Windows** para ser executado em horários determinados.

## Dependências
O script utiliza as seguintes bibliotecas Python padrão, que já estão inclusas na instalação do Python 3:
- `os`: Para manipulação de arquivos e diretórios.
- `shutil`: Para operações de movimentação de arquivos.
- `datetime`: Para geração de timestamps no arquivo de log.

Para gerar o executável, é necessário o **PyInstaller**, que pode ser instalado separadamente.

### Instalação das Dependências
1. **Instalar o Python 3**:
   - Baixe e instale o Python 3 a partir do site oficial: [python.org](https://www.python.org/downloads/).
   - Certifique-se de adicionar o Python ao PATH durante a instalação.

2. **Instalar o PyInstaller**:
   - Abra um terminal (Prompt de Comando) no servidor.
   - Execute o seguinte comando para instalar o PyInstaller:
     ```bash
     pip install pyinstaller
     ```

## Geração do Executável
O script foi convertido em um executável utilizando o PyInstaller para facilitar a execução no servidor Windows Server 2012 R2. Para gerar o executável, siga os passos abaixo:
1. Abra um terminal no diretório onde está o script `appLocAzul-v2.py`.
2. Execute o comando:
   ```bash
   pyinstaller --onefile appLocAzul-v2.py
   ```
3. O executável será gerado na pasta `dist` com o nome `appLocAzul-v2.exe`.

O executável gerado inclui todas as dependências necessárias, eliminando a necessidade de instalar o Python ou bibliotecas adicionais no servidor.

## Configuração no Agendador de Tarefas
O executável `appLocAzul-v2.exe` foi configurado no **Agendador de Tarefas do Windows** para ser executado automaticamente em horários específicos. Para configurar uma tarefa semelhante:
1. Abra o **Agendador de Tarefas** no Windows Server 2012 R2.
2. Crie uma nova tarefa:
   - Acesse **Criar Tarefa** no menu **Ações**.
   - Na aba **Geral**, defina um nome para a tarefa (ex.: "Processamento Azul").
   - Marque a opção **Executar independentemente do usuário estar logado ou não** e configure com uma conta de usuário com permissões adequadas.
3. Na aba **Gatilhos**, configure o horário desejado para execução (ex.: diariamente às 08:00).
4. Na aba **Ações**, adicione uma ação do tipo **Iniciar um Programa** e aponte para o caminho do executável (`appLocAzul-v2.exe`).
5. Na aba **Condições** e **Configurações**, ajuste conforme necessário (ex.: reiniciar em caso de falha).
6. Salve a tarefa e teste a execução.

## Como Executar
1. **Execução Manual do Script** (caso não utilize o executável):
   - Instale o Python 3 no servidor, caso ainda não esteja instalado.
   - Verifique se as pastas de origem e destino estão acessíveis e possuem as permissões corretas para leitura e escrita.
   - Coloque o script `appLocAzul-v2.py` em um diretório acessível no servidor.
   - Abra um terminal (Prompt de Comando) no servidor.
   - Navegue até o diretório onde o script está localizado.
   - Execute o comando:
     ```bash
     python appLocAzul-v2.py
     ```

2. **Execução do Executável**:
   - Coloque o arquivo `appLocAzul-v2.exe` em um diretório acessível no servidor.
   - Execute o arquivo diretamente ou aguarde a execução automática pelo Agendador de Tarefas.

3. **Saída**:
   - Os arquivos processados serão movidos para a pasta de destino.
   - Um arquivo de log (`processing_log.txt`) será gerado na pasta de destino, contendo o registro de todas as operações realizadas.

## Estrutura do Código
- **Constantes**:
  - `SOURCE_FOLDER`: Caminho da pasta de origem dos arquivos.
  - `DESTINATION_FOLDER`: Caminho da pasta de destino dos arquivos processados.
- **Função `modify_file`**:
  - Lê o arquivo, verifica a presença da linha `A-CIA AEREA;AD`, realiza modificações, salva o arquivo na pasta de destino e remove o original.
- **Função `process_folder`**:
  - Gerencia o processamento de todos os arquivos na pasta de origem, cria o arquivo de log e coordena a execução da função `modify_file`.

## Desenvolvimento
Este script foi desenvolvido de forma colaborativa com o auxílio da inteligência artificial **Grok 3**, criada pela xAI. A IA foi utilizada para estruturar o código, implementar as funcionalidades e garantir a robustez do script.

## Notas
- **Codificação**: O script tenta diferentes codificações para ler os arquivos, garantindo maior compatibilidade com diferentes formatos de texto.
- **Tratamento de Erros**: O script registra erros no arquivo de log, como falhas ao ler/escrever arquivos ou problemas ao acessar as pastas.
- **Permissões**: Certifique-se de que o usuário que executa o script ou o executável tem permissões de leitura/escrita nas pastas de origem e destino.
- **Logs**: O arquivo `processing_log.txt` é criado na pasta de destino e contém detalhes sobre o processamento, incluindo arquivos ignorados, modificados ou erros encontrados.
- **Agendamento**: O agendamento no servidor garante que o processamento ocorra automaticamente, mas é recomendável monitorar os logs regularmente para verificar possíveis erros.

## Correção de Problemas com BOM (Byte Order Mark) - 29 de Setembro de 2025
### Problema Identificado
Em 29 de setembro de 2025, foi identificado um erro em arquivos processados, onde o validador downstream reportava: "O arquivo tem que começar por 'AIR' e começa com 'Ï»¿AIR-BLK204;7...'". Esse erro ocorria devido à presença de um BOM UTF-8 (`\xef\xbb\xbf`) no início dos arquivos de origem, que era interpretado como caracteres literais ("Ï»¿") quando lido em codificações como `latin1` ou `cp1252`. Isso resultava em arquivos processados que não atendiam ao requisito do validador de começar com "AIR".

### Solução Implementada
A função `modify_file` no script `appLocAzul-v2.py` foi atualizada para:
- Ler os arquivos em modo binário (`'rb'`) para inspecionar os bytes diretamente.
- Verificar e remover o BOM UTF-8 (`\xef\xbb\xbf`) do início do conteúdo, se presente.
- Decodificar o conteúdo restante com as codificações `utf-8`, `latin1` ou `cp1252`, garantindo que o BOM não seja interpretado como texto.
- Registrar

## Correção de Problemas com classe UU UU - 25 de Novembro de 2025
### Problema Identificado
Em 25 de Novembro de 2025, foi identificado um erro em arquivos processados, onde o validador downstream reportava: "Classe deve ter uma posição:N'". Esse erro ocorria devido à presença do caracter UU UU no arquivo. Isso resultava em arquivos processados que não atendiam ao requisito do validador de começar com "U U".
- Ler os arquivos loaliza o registro H.
- Verificar e remover o UU UU, se presente, substituindo por U U.
