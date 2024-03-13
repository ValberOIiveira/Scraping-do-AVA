from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializar o navegador
driver = webdriver.Chrome()

try:
    # Navegar até a página de login da UFMS
    driver.get("https://ava.ufms.br/login/index.php")

    # Inserir as informações de login
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.send_keys("seu_nome")
    password.send_keys("sua_senha")

    # Clicar no botão de login
    login_btn = driver.find_element(By.ID, "loginbtn")
    login_btn.click()

    # Navegar diretamente para o link do calendário
    driver.get("https://ava.ufms.br/calendar/view.php?view=month")

    # Aguardar até que o botão de mês seja visível
    botao_mes = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "calendarviewdropdown"))
    )

    # Clicar no botão de mês
    botao_mes.click()

    # Aguardar até que o link de "Próximos eventos" seja visível
    proximos_eventos = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Próximos eventos')]"))
    )

    # Clicar no link de "Próximos eventos"
    proximos_eventos.click()

    # Aguardar até que os eventos sejam visíveis
    eventos = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "event"))
    )

    # Extrair os nomes dos eventos e suas datas de entrega
    dados_eventos = []
    for evento in eventos:
        nome_evento_elemento = evento.find_element(By.CLASS_NAME, "name")
        nome_evento = nome_evento_elemento.text
        data_elemento = evento.find_element(By.XPATH, ".//div[contains(@class, 'row')][1]//div[contains(@class, 'col-11')]")
        data_entrega = data_elemento.text
        dados_eventos.append((nome_evento, data_entrega))

    # Exibir os dados dos eventos
    for nome, data in dados_eventos:
        print(f"Nome do Evento: {nome}")
        print(f"Data de Entrega: {data}\n")

    # Abrir um arquivo em modo de escrita ('w')
    with open("dados_eventos.txt", "w") as arquivo:
        # Escrever os dados dos eventos no arquivo
        for nome, data in dados_eventos:
            arquivo.write(f"Nome do Evento: {nome}\n")
            arquivo.write(f"Data de Entrega: {data}\n\n")

    # Informar ao usuário que os dados foram salvos
    print("Os dados foram salvos no arquivo 'dados_eventos.txt'")

    # Aguardar para verificar os resultados
    input("Verifique se as ações foram concluídas corretamente. Pressione Enter para fechar o navegador...")

finally:
    # Fechar o navegador
    driver.quit()
