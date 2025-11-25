import os
import shutil
from datetime import datetime

# Versao 2 - 25/11/2025
# Constantes para os caminhos das pastas
SOURCE_FOLDER = r"\\REGENTEAPP\Senior\Regente\GDS\AGUARDANDO"
DESTINATION_FOLDER = r"\\REGENTEAPP\Senior\Regente\GDS"
#SOURCE_FOLDER = r"C:\Users\israel.ruiz\Desktop\TARUMAN\com erro"
#DESTINATION_FOLDER = r"C:\Users\israel.ruiz\Desktop\TARUMAN\com erro\ajustados"

def modify_file(file_path, log_file_path, destination_folder):
    # Variável para código da companhia
    has_required_line = False
    used_encoding = None

    # Ler arquivo em modo binário
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
    except Exception as e:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Erro ao ler {file_path} em binário: {str(e)}\n")
        return False

    # Remover BOM UTF-8 se existir
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"BOM UTF-8 detectado e removido em {file_path}.\n")

    # Tentar decodificação
    for enc in ['utf-8', 'latin1', 'cp1252']:
        try:
            text = content.decode(enc)
            used_encoding = enc
            break
        except:
            continue

    if used_encoding is None:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Erro ao decodificar {file_path}.\n")
        return False

    lines = text.splitlines(keepends=True)

    # Confirmar se é arquivo da Azul
    for line in lines:
        if "A-CIA AEREA;AD" in line:
            has_required_line = True
            break

    modified_lines = []
    modified = False

    # Posição fixa definida pelo layout (index = 65)
    CAMPO_INICIO = 65

    if has_required_line:
        for line in lines:
            new_line = line

            # Regras já existentes
            if line.startswith("A-CIA AEREA;AD 5770") or line.startswith("A-CIA AEREA;AD 9030"):
                new_line = (
                    line.replace("A-CIA AEREA;AD 5770", "A-CIA AEREA;AD 4130")
                        .replace("A-CIA AEREA;AD 9030", "A-CIA AEREA;AD 4130")
                )
                modified = True

            elif line.startswith("T-K577-") or line.startswith("T-#0413-") or line.startswith("T-K903-"):
                new_line = (
                    line.replace("T-K577-", "T-K413-")
                        .replace("T-#0413-", "T-K413-")
                        .replace("T-K903-", "T-K413-")
                )
                modified = True

            # ------------------------------------------------------
            # NOVA REGRA DEFINITIVA: corrigir linha H com index = 65
            # Substituir "UU UU" → "U U" (encurtando a linha)
            # ------------------------------------------------------
            elif line.startswith("H"):
                sufixo = line[CAMPO_INICIO:]  # tudo a partir da posição 65

                if "UU UU" in sufixo:
                    # Substituição correta: encolhe o bloco
                    sufixo_corrigido = sufixo.replace("UU UU", "U U", 1)
                    new_line = line[:CAMPO_INICIO] + sufixo_corrigido
                    modified = True

            modified_lines.append(new_line)

    else:
        modified_lines = lines
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"arquivo {file_path} ignorado: não contém linha 'A-CIA AEREA;AD'.\n")

    # Salvar arquivo corrigido
    destination_file_path = os.path.join(destination_folder, os.path.basename(file_path))

    try:
        with open(destination_file_path, 'w', encoding=used_encoding, newline='') as file:
            file.writelines(modified_lines)

        msg = f"Arquivo {file_path} movido para {destination_file_path}"
        msg += " com modificações.\n" if modified else " sem modificações.\n"

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(msg)

        # Remover original
        try:
            os.remove(file_path)
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Arquivo original {file_path} removido.\n")
        except Exception as e:
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Erro ao remover arquivo original {file_path}: {str(e)}\n")

        return True

    except Exception as e:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Erro ao escrever {destination_file_path}: {str(e)}\n")
        return False


def process_folder():
    source_folder = SOURCE_FOLDER
    destination_folder = DESTINATION_FOLDER

    if not os.path.isdir(source_folder):
        log_file_path = os.path.join(destination_folder, "processing_log.txt")
        os.makedirs(destination_folder, exist_ok=True)
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Erro: Pasta {source_folder} não existe.\n")
        return

    os.makedirs(destination_folder, exist_ok=True)

    log_file_path = os.path.join(destination_folder, "processing_log.txt")
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(
            f"Log de Processamento - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 50}\n"
        )

    arquivos = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    if not arquivos:
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write("Nenhum arquivo encontrado.\n")
        return

    for nome in arquivos:
        caminho = os.path.join(source_folder, nome)
        modify_file(caminho, log_file_path, destination_folder)

    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write("Processamento finalizado.\n")


if __name__ == "__main__":
    process_folder()
