import os
import shutil
from datetime import datetime

# Constantes para os caminhos das pastas
SOURCE_FOLDER = r"\\REGENTEAPP\Senior\Regente\GDS\AGUARDANDO"
DESTINATION_FOLDER = r"\\REGENTEAPP\Senior\Regente\GDS"
#SOURCE_FOLDER = r"C:\Users\israe\Desktop\TARUMAN\AIR_SEP_ERROS"
#DESTINATION_FOLDER = r"C:\Users\israe\Desktop\TARUMAN\AIR_SEP_ERROS\GDS"

def modify_file(file_path, log_file_path, destination_folder):
    # Variável para código da companhia
    sigla = ""
    has_required_line = False
    
    # Ler em modo binário para lidar com BOM
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
    except Exception as e:
        log_message = f"Erro ao ler {file_path} em binário: {str(e)}\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return False
    
    # Remover BOM UTF-8 se presente
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
        log_message = f"BOM UTF-8 detectado e removido em {file_path}.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
    
    # Tentar decodificar o conteúdo (sem BOM)
    encodings = ['utf-8', 'latin1', 'cp1252']
    lines = None
    used_encoding = None
    for encoding in encodings:
        try:
            text = content.decode(encoding)
            lines = text.splitlines(keepends=True)  # Simula readlines() preservando newlines
            used_encoding = encoding
            break
        except Exception as e:
            continue
    
    if lines is None:
        log_message = f"Erro ao decodificar {file_path}: Todas as codificações falharam.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return False
    
    log_message = f"Arquivo {file_path} lido com sucesso usando encoding '{used_encoding}'.\n"
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_message)
    
    # O resto da função permanece igual (verificação de "A-CIA AEREA;AD", modificações, etc.)
    # ...    
    # Verificar linha A-CIA AEREA
    for line in lines:
        if line.startswith("A-CIA AEREA;AD"):
            parts = line.split(';')
            if len(parts) > 1:
                code_parts = parts[1].strip().split()
                if len(code_parts) == 2 and code_parts[0] == "AD":
                    sigla = code_parts[0]
                    has_required_line = True
    
    # Modificar linhas se for companhia AD
    modified_lines = []
    modified = False
    
    if has_required_line:
        for line in lines:
            new_line = line
            if line.startswith("A-CIA AEREA;AD 5770") or line.startswith("A-CIA AEREA;AD 9030"):
                new_line = line.replace("A-CIA AEREA;AD 5770", "A-CIA AEREA;AD 4130").replace("A-CIA AEREA;AD 9030", "A-CIA AEREA;AD 4130")
                modified = True
            elif line.startswith("T-K577-") or line.startswith("T-#0413-") or line.startswith("T-K903-"):
                new_line = line.replace("T-K577-", "T-K413-").replace("T-#0413-", "T-K413-").replace("T-K903-", "T-K413-")
                modified = True
            modified_lines.append(new_line)
    else:
        modified_lines = lines
        log_message = f"arquivo {file_path} ignorado: não contém linha 'A-CIA AEREA;AD'.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
    
    # Salvar arquivo na pasta de destino
    destination_file_path = os.path.join(destination_folder, os.path.basename(file_path))
    try:
        with open(destination_file_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
        log_message = f"Arquivo {file_path} movido para {destination_file_path}"
        if modified:
            log_message += " com modificações.\n"
        else:
            log_message += " sem modificações.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        
        # Remover arquivo original da pasta de origem
        try:
            os.remove(file_path)
            log_message = f"Arquivo original {file_path} removido após processamento.\n"
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
        except Exception as e:
            log_message = f"Erro ao remover arquivo original {file_path}: {str(e)}\n"
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_message)
        return True
    except Exception as e:
        log_message = f"Erro ao escrever {destination_file_path}: {str(e)}\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return False

def process_folder():
    # Usar constantes para as pastas
    source_folder = SOURCE_FOLDER
    destination_folder = DESTINATION_FOLDER
    
    if not os.path.isdir(source_folder):
        log_file_path = os.path.join(destination_folder, "processing_log.txt")
        os.makedirs(destination_folder, exist_ok=True)
        log_message = f"Erro: A pasta {source_folder} não existe.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return
    
    # Criar pasta de destino se não existir
    os.makedirs(destination_folder, exist_ok=True)
    
    # Criar caminho para o arquivo de log na pasta de destino
    log_file_path = os.path.join(destination_folder, "processing_log.txt")
    
    # Adicionar cabeçalho ao arquivo de log
    log_message = f"Log de Processamento - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n"
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(log_message)
    
    # Listar todos os arquivos na pasta de origem
    all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    if not all_files:
        log_message = f"Nenhum arquivo encontrado na pasta {source_folder}.\n"
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)
        return
    
    # Processar cada arquivo
    for file_name in all_files:
        file_path = os.path.join(source_folder, file_name)
        modify_file(file_path, log_file_path, destination_folder)
    
    log_message = "Processamento finalizado.\n"
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_message)

if __name__ == "__main__":
    process_folder()