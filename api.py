from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# Exemplo de scraping de eventos do Sympla usando Selenium
def fetch_eventos_sympla_selenium():
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    base_url = 'https://www.sympla.com.br/eventos/corporativo?c=em-destaque&ordem=month-trending-score&page={}'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    eventos = []
    eventos_ids = set()
    driver = None
    total_paginas = 1
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Primeiro, descobre o total de páginas
        driver.get(base_url.format(1))
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ig8y7h0.ig8y7h2')))
        try:
            # Busca todos os botões de página (números)
            botoes_pag = driver.find_elements(By.XPATH, "//button[not(@disabled)]")
            numeros = []
            for b in botoes_pag:
                txt = b.text.strip()
                if txt.isdigit():
                    numeros.append(int(txt))
            if numeros:
                total_paginas = max(numeros)
        except Exception as e:
            print(f"[DEBUG] Falha ao detectar total de páginas: {e}")
        for pagina in range(1, total_paginas+1):
            driver.get(base_url.format(pagina))
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ig8y7h0.ig8y7h2')))
            bloco = driver.find_element(By.CSS_SELECTOR, 'div.ig8y7h0.ig8y7h2')
            cards = bloco.find_elements(By.CSS_SELECTOR, 'a.sympla-card.pn67h10.pn67h12')
            print(f"Página {pagina}/{total_paginas} processada. {len(cards)} eventos encontrados.")
            eventos_pagina = 0
            for card in cards:
                try:
                    event_id = card.get_attribute('href')
                    nome = card.find_element(By.CSS_SELECTOR, 'h3.pn67h1a').text.strip()
                    local = card.find_element(By.CSS_SELECTOR, 'p.pn67h1c').text.strip()
                    data_elem = card.find_element(By.CSS_SELECTOR, 'div.qtfy415.qtfy413.qtfy416')
                    data = data_elem.text.replace('\n', '').replace('\r', '').strip()
                    datas = data.split(' a ')
                    data_inicio = datas[0].strip()
                    data_termino = datas[-1].strip() if len(datas) > 1 else data_inicio
                    def parse_data(d):
                        import re
                        meses = {
                            'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
                            'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12',
                            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04', 'maio': '05', 'junho': '06',
                            'julho': '07', 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
                        }
                        d = d.strip().lower()
                        match = re.search(r'(\d{1,2}) de ([a-zçãé]+)', d)
                        if match:
                            dia = match.group(1)
                            mes = match.group(2)
                            mes3 = mes[:3]
                            mes_num = meses.get(mes3) or meses.get(mes)
                            if mes_num:
                                return f"2025-{mes_num}-{int(dia):02d}"
                        try:
                            return datetime.strptime(d, '%d/%m/%Y').strftime('%Y-%m-%d')
                        except Exception:
                            pass
                        return ''

                    data_inicio_fmt = parse_data(data_inicio)
                    data_termino_fmt = parse_data(data_termino)
                    if data_inicio_fmt and event_id and event_id not in eventos_ids:
                        eventos.append({
                            'data_inicio': data_inicio_fmt,
                            'data_termino': data_termino_fmt,
                            'nome_evento': nome,
                            'tipo': 'Evento Corporativo',
                            'estado': local,
                            'impacto_aviacao': 'Baixo',
                        })
                        eventos_ids.add(event_id)
                        eventos_pagina += 1
                except Exception:
                    continue
    except Exception as e:
        print(f"Erro ao buscar Sympla Selenium: {e}")
    finally:
        if driver:
            driver.quit()
    return eventos
    try:
        resp = requests.get(url, verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        cards = soup.find_all('div', class_='sc-1fcmfeb-0')
        for card in cards:
            nome = card.find('h2')
            data = card.find('span', class_='sc-1fcmfeb-6')
            local = card.find('span', class_='sc-1fcmfeb-7')
            if nome and data:
                nome_evento = nome.get_text(strip=True)
                datas = data.get_text(strip=True).split(' a ')
                data_inicio = datas[0].strip()
                data_termino = datas[-1].strip() if len(datas) > 1 else data_inicio
                # Tenta converter para formato ISO
                try:
                    data_inicio_fmt = datetime.strptime(data_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
                    data_termino_fmt = datetime.strptime(data_termino, '%d/%m/%Y').strftime('%Y-%m-%d')
                except:
                    data_inicio_fmt = data_inicio
                    data_termino_fmt = data_termino
                eventos.append({
                    'data_inicio': data_inicio_fmt,
                    'data_termino': data_termino_fmt,
                    'nome_evento': nome_evento,
                    'tipo': 'Evento Corporativo',
                    'estado': local.get_text(strip=True) if local else 'Desconhecido',
                    'impacto_aviacao': 'Baixo',
                })
    except Exception as e:
        print(f"Erro ao buscar Sympla: {e}")
    return eventos
from bs4 import BeautifulSoup
# Exemplo de scraping de eventos de uma página HTML
def fetch_eventos_html_exemplo():
    url = 'https://www.calendarr.com/brasil/feriados-nacionais-2025/'
    eventos = []
    try:
        resp = requests.get(url, verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table')
        if table:
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    data = cols[0].get_text(strip=True)
                    nome = cols[1].get_text(strip=True)
                    # data no formato dd/mm
                    data_inicio = f"2025-{data.split('/')[1]}-{data.split('/')[0]}"
                    eventos.append({
                        'data_inicio': data_inicio,
                        'data_termino': data_inicio,
                        'nome_evento': nome,
                        'tipo': 'Feriado Nacional',
                        'estado': 'Todos',
                        'impacto_aviacao': 'Médio'
                    })
    except Exception as e:
        print(f"Erro ao buscar eventos HTML: {e}")
    return eventos

import pandas as pd
import requests
from datetime import datetime, timedelta


# Função principal para buscar feriados nacionais do IBGE/Gov.br
def fetch_eventos_nacionais():
    url = 'https://servicodados.ibge.gov.br/api/v2/calendario/feriados/2025'
    eventos = []
    try:
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            for feriado in data:
                eventos.append({
                    'data_inicio': feriado.get('date', ''),
                    'data_termino': feriado.get('date', ''),
                    'nome_evento': feriado.get('name', ''),
                    'tipo': 'Feriado Nacional',
                    'estado': 'Todos',
                    'impacto_aviacao': 'Médio'
                })
    except Exception as e:
        print(f"Erro ao buscar Gov.br: {e}")
    return eventos

def calcular_dia_semana(data_inicio):
    data = datetime.strptime(data_inicio, '%Y-%m-%d')
    return data.strftime('%A')

def calcular_dias_restantes(data_inicio):
    hoje = datetime.now()
    data = datetime.strptime(data_inicio, '%Y-%m-%d')
    return (data - hoje).days

def verificar_possivel_emenda(data_inicio, data_termino):
    data = datetime.strptime(data_inicio, '%Y-%m-%d')
    if data.weekday() == 1 or data.weekday() == 3:
        return 'Sim'
    return 'Não'

def montar_dataframe_eventos():
    # Para scraping de HTML, troque a função abaixo:
    # eventos = fetch_eventos_html_exemplo()
    # eventos = fetch_eventos_sympla()
    eventos = fetch_eventos_sympla_selenium()
    df = pd.DataFrame(eventos)
    if df.empty:
        print('Nenhum evento foi encontrado.')
        return df
    df['Dia da semana que iniciará'] = df['data_inicio'].apply(calcular_dia_semana)
    df['Dias restantes para o evento'] = df['data_inicio'].apply(calcular_dias_restantes)
    df['Se terá possível emenda'] = df.apply(lambda row: verificar_possivel_emenda(row['data_inicio'], row['data_termino']), axis=1)
    # Renomear colunas para o formato solicitado
    df = df.rename(columns={
        'data_inicio': 'data inicio',
        'data_termino': 'data termino',
        'nome_evento': 'nome do evento',
        'tipo': 'Tipo',
        'estado': 'Estado que ocorrerá',
        'impacto_aviacao': 'Impacto para a aviação',
    })
    return df

if __name__ == "__main__":
    df_eventos = montar_dataframe_eventos()
    print(df_eventos)
    if not df_eventos.empty:
        df_eventos.to_csv('eventos_sympla.csv', index=False, encoding='utf-8-sig')
        print('Arquivo eventos_sympla.csv exportado com sucesso!')
