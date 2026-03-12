# Magic Statues

**Magic Statues** é uma aplicação desktop desenvolvida em **Python com PyQt5** para ajudar jogadores do **Magic Campus** a gerenciar o progresso no evento de caça às **Estátuas**.

Durante o evento, um tipo especial de inimigo aparece nos mapas do jogo. Esse inimigo é conhecido pelos jogadores como **"Estátua"**. Como existem vários mapas com diferentes requisitos de nível, pode ser fácil se perder sobre quais já foram feitos ou ainda precisam ser completados.

O objetivo desta ferramenta é facilitar o controle desses mapas para tornar a progressão do evento mais organizada.

---

## Funcionalidades

* Lista de mapas organizados por:

  * **Nome do mapa**
  * **Mundo**
  * **Intervalo de nível recomendado**

* Sistema de status para cada mapa:

  * **Habilitado** (verde) → mapa ainda pode ser feito
  * **Derrotado** (vermelho) → estátua já derrotada naquele mapa

* Sistema de **filtro por status**

  * Nenhum
  * Habilitado
  * Derrotado

* **Filtro por nível do jogador**

* Botão para **resetar todos os mapas**

* **Salvamento automático do progresso em JSON**

* **Carregamento automático dos estados ao abrir o programa**

---

## Como funciona

Cada mapa possui:

* Nome do mapa
* Mundo correspondente
* Intervalo de nível recomendado
* Botão para marcar se a **Estátua daquele mapa já foi derrotada**

Isso permite que o jogador acompanhe facilmente seu progresso durante o evento.

---

## Salvamento de progresso

Os estados são armazenados no arquivo:

```
status_statues.json
```

Exemplo:

```json
{
  "Espaço Zen": "Derrotado",
  "Planalto do Sol Nascente": "Habilitado"
}
```

Quando o programa é iniciado novamente, ele **carrega automaticamente os estados salvos**.

---

## Requisitos

* Python **3.8 ou superior**
* PyQt5

Instalar dependência:

```
pip install PyQt5
```

---

## Como executar

Execute o arquivo principal:

```
python main.py
```

---

## Estrutura do projeto

```
Magic-Statues/
│
├── main.py
├── status_statues.json
└── README.md
```

---

## Objetivo do projeto

Este projeto foi criado para ajudar jogadores de **Magic Campus** a organizarem a caça às **Estátuas** durante o evento, evitando confusão sobre quais mapas já foram concluídos.

A ferramenta permite que o jogador:

* Controle facilmente quais estátuas já derrotou
* Filtre mapas de acordo com seu nível
* Organize sua rota de caça durante o evento

---

## Tecnologias utilizadas

* **Python**
* **PyQt5**
* **JSON** para persistência de dados

---

## Possíveis melhorias futuras

* Interface visual aprimorada
* Contador de estátuas derrotadas
* Adicionar mais mapas automaticamente
* Backup automático do progresso
* Versão compilada para **Windows (.exe)**

---

Projeto desenvolvido para auxiliar a comunidade de jogadores de **Magic Campus** e para estudo de desenvolvimento de interfaces gráficas em Python.
