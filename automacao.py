from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
    print("Conectado com sucesso no Chrome!")
except Exception as e:
    print("Erro: O chrome não está aberto no modo de automação.")
    exit()

print("\nAGUARDANDO COMANDO")
print("1. Cadastrando o cliente.")
print("2. Deixar aberto na aba de planos")
print("--------------------------")
input("Clicar no ENTER APENAS quando estiver na tela dos planos")

def inativar_plano_atual():
    # ordem 1. Abre o campo de Status
    campo_status = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ativo')] | //mat-select | //*[contains(text(), 'Status')]/following::div[1]"))
    )
    campo_status.click()
    time.sleep(0.6)
    
    # ordem 2. Clica na opção 'Inativo'
    opcao_inativo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//mat-option//span[contains(text(), 'Inativo')] | //*[text()='Inativo']"))
    )
    opcao_inativo.click()
    time.sleep(0.6)
    
    # ordem 3. Clica no botão ALTERAR azul escuro (do topo da página)
    botao_alterar_topo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div/div[2]/div/button[2]'))
    )
    botao_alterar_topo.click()
    time.sleep(0.8)
    
    # ordem4. Confirma clicando no botão ALTERAR dentro do Modal
    botao_confirmar_modal = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[4]/div/div/div[2]/button[2]'))
    )
    botao_confirmar_modal.click()
    print(" Alteração salva")
    time.sleep(1.8)
    
    # 5. ordem Clica no botão VOLTAR para retornar à lista de planos
    botao_voltar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div/div[2]/div/button[1]'))
    )
    botao_voltar.click()
    time.sleep(1.8)

# LOOP PRINCIPAL PELAS PÁGINAS
for pagina in range(1, 6):
    print(f"\nAnalisando a Página {pagina} da lista...")
    time.sleep(2)
    
    # Pega a quantidade real de linhas que existem na tabela ao carregar a página
    linhas_tabela = driver.find_elements(By.XPATH, "//table/tbody/tr | //tbody/tr | //tr[@mat-row]")
    total_linhas = len(linhas_tabela)
    print(f"Encontradas {total_linhas} linhas no total nesta página.")
    
    #Usando um índice rígido (0, 1, 2, 3...)
    for indice in range(total_linhas):
        print(f"Processando a linha {indice + 1} de {total_linhas} (Página {pagina})...")
        
        try:
            # Recarrega a tabela para evitar o erro de elemento antigo
            linhas_tabela = driver.find_elements(By.XPATH, "//table/tbody/tr | //tbody/tr | //tr[@mat-row]")
            
            # Clica estritamente na linha da vez (0, depois 1, depois 2...)
            linhas_tabela[indice].click()
            time.sleep(1.2)
            
            # Executa a inativação interna
            inativar_plano_atual()
            
        except Exception as e:
            # Se a linha sumiu ou deu erro, ele avança para tentar a próxima linha sem quebrar o código
            print(f"Erro ou linha já processada no índice {indice + 1}. Pulando para o próximo...")
            continue
            
    # SÓ DEPOIS de passar por todas as linhas da página ele tenta avançar
    if pagina < 5:
        proxima = pagina + 1
        print(f"Todas as linhas da página {pagina} foram testadas. Indo para a página {proxima}...")
        try:
            botao_proxima = driver.find_element(By.XPATH, f"//*[text()='{proxima}'] | //*[contains(@aria-label, '{proxima}')]")
            botao_proxima.click()
            time.sleep(2.5)
        except Exception:
            input(f"Não achei o botão automático. Clique manualmente na página {proxima} no Chrome e dê ENTER aqui...")

print("\nTodos planos inativados!")