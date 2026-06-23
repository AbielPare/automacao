from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurações do Chrome Debugger
chrome_options = Options()
chrome_options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

try:
    service = Service(
        "/home/vicensopolanociotta/.cache/selenium/chromedriver/linux64/149.0.7827.115/chromedriver"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    print("Conectado com sucesso no Chrome!")

except Exception as e:
    print(f"Erro ao conectar: {e}")
    exit()

print("\nAGUARDANDO COMANDO")
print("1. Cadastrando o cliente.")
print("2. Deixar aberto na aba de planos")
print("--------------------------")
input("Clicar no ENTER APENAS quando estiver na tela dos planos")


def inativar_plano_atual():
    # 1. Clicar no campo de Status (Ativo)
    campo_status = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ativo')] | //mat-select | //*[contains(text(), 'Status')]/following::div[1]"))
    )
    campo_status.click()
    time.sleep(0.6)
    
    # 2. Selecionar a opção Inativo
    opcao_inativo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//mat-option//span[contains(text(), 'Inativo')] | //*[text()='Inativo']"))
    )
    opcao_inativo.click()
    time.sleep(0.6)
    
    # 3. Clicar no botão ALTERAR do topo
    botao_alterar_topo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ALTERAR')] | //span[contains(text(), 'ALTERAR')] | //button[contains(text(), 'Alterar')] | //span[contains(text(), 'Alterar')]"))
    )
    driver.execute_script("arguments[0].click();", botao_alterar_topo)
    time.sleep(0.8)
    
    # 4. Confirmar no modal de aviso
    botao_confirmar_modal = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//mat-dialog-container//button[contains(., 'ALTERAR')] | //div[contains(@class, 'modal')]//button[contains(., 'Alterar')] | (//button[contains(., 'ALTERAR') or contains(., 'Alterar')])[2]"))
    )
    driver.execute_script("arguments[0].click();", botao_confirmar_modal)
    print(" Alteração salva com sucesso!")
    time.sleep(1.8)
    
    # 5. Clicar em Voltar (O site vai resetar para a página 1 após isso)
    botao_voltar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VOLTAR')] | //button[contains(text(), 'Voltar')] | //span[contains(text(), 'Voltar')] | //*[@id='app']/div/main/div/div/div[2]/div/button[1]"))
    )
    driver.execute_script("arguments[0].click();", botao_voltar)
    time.sleep(1.8)


# ==============================================================================
# LOOP PRINCIPAL CORRIGIDO: FIXADO NO ÍNDICE 0 (TOPO DOS ATIVOS)
# ==============================================================================

for pagina in range(1, 6):
    print(f"\n--- Analisando a Página {pagina} ---")
    
    # IMPORTANTE: Forçamos o índice a ser SEMPRE 0.
    # Como os planos inativados mudam de cor, o próximo "Ativo" vira o novo índice 0.
    indice = 0
    
    while True:
        try:
            # 1. SE O SITE RESETOU PARA A PÁGINA 1, FORÇA A VOLTA PARA A PÁGINA QUE ESTÁVAMOS
            if pagina > 1:
                try:
                    botao_pag = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[text()=' {pagina} ' or text()='{pagina}'] | //ul/li[contains(., '{pagina}')]"))
                    )
                    classe_botao = str(botao_pag.get_attribute("class"))
                    if "active" not in classe_botao and "selected" not in classe_botao:
                        print(f"Identificado reset do site. Navegando de volta para a Página {pagina}...")
                        botao_pag.click()
                        time.sleep(2.5)  # Tempo crucial para a tabela carregar os dados novos
                except Exception:
                    pass

            # 2. CAPTURA APENAS AS LINHAS QUE CONTÉM O STATUS "ATIVO" (TAG VERDE)
            linhas_ativas = driver.find_elements(By.XPATH, "//tr[.//span[contains(text(), 'Ativo')]] | //tr[contains(., 'Ativo')]")
            total_ativas = len(linhas_ativas)
            
            # Se zerar os ativos da página, encerra o loop dessa página
            if total_ativas == 0:
                print(f"Não há mais planos 'Ativos' pendentes na Página {pagina}.")
                break
                
            print(f"Encontrados {total_ativas} planos ativos. Processando o primeiro da lista...")
            
            # 3. CLICA SEMPRE NO PRIMEIRO PLANO ATIVO DISPONÍVEL (ÍNDICE 0)
            linhas_ativas[0].click()
            time.sleep(1.5)
            
            # 4. EXECUTA A ROTINA DE INATIVAÇÃO e VOLTA
            inativar_plano_atual()
            
            # Mantém em 0 para a próxima rodada pegar o novo topo
            indice = 0 
            
        except Exception as e:
            print(f"Aviso na página {pagina}. Tentando re-sincronizar o estado da tela...")
            time.sleep(2.5)
            # NÃO incrementamos o índice aqui para ele não pular registros. 
            # Ele tentará ler o topo da lista novamente na próxima linha do loop.
            indice = 0 

    # 5. AVANÇAR PARA A PRÓXIMA PÁGINA
    if pagina < 5:
        proxima = pagina + 1
        print(f"Todos os ativos da página {pagina} limpos. Avançando para a página {proxima}...")
        try:
            botao_proxima = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[text()=' {proxima} ' or text()='{proxima}'] | //ul/li[contains(., '{proxima}')]"))
            )
            botao_proxima.click()
            time.sleep(2.5)
        except Exception:
            input(f"Aviso: Não consegui clicar na página {proxima} automaticamente. Clique nela manualmente e pressione ENTER aqui...")

print("\n[SUCESSO] Todos os planos ativos das 5 páginas foram processados!")