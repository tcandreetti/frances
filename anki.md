# 🃏 Anki: os cartões do curso no celular

O Anki é um app de **cartões de memória** que mostra cada palavra **na hora certa de revisar**. 🧠

Ele faz sozinho a revisão espaçada: o que você sabe aparece pouco, o que você erra aparece mais.

Volte ao [hub](README.md) · [Plano de estudo](plano-de-estudo.md) · [Progresso](progresso.md)

## 📦 O deck do curso

📥 **[Baixar o deck "Francês da Thaís" (.apkg)](https://tcandreetti.github.io/frances/anki/frances-thais.apkg)**

- Um **subdeck por aula** (Aulas 01–06 e 13–20).
- Cada palavra ou frase vira **2 cartões**: francês → português e português → francês.
- Palavras com **artigo** (*le vin, la mer, l'eau*): aprenda sempre os dois juntos.
- **Todo cartão tem áudio** com voz francesa. 🔊

## 1️⃣ Instalar (uma vez só)

1. Abra a **Play Store** no celular Android.
2. Procure **AnkiDroid** (o ícone é uma estrela azul). É **grátis**.
3. Instale e abra. Se ele pedir permissão para acessar arquivos, toque em **Permitir**.

💡 O AnkiDroid é o app oficial gratuito para Android. Não precisa criar conta para começar.

💡 Com o celular em português, o app chama o deck de **baralho**. É a mesma coisa.

## 2️⃣ Importar o deck

**Jeito 1 · pelo arquivo (mais fácil):**

1. No celular, toque no link **Baixar o deck** acima.
2. Quando o download terminar, toque na notificação (ou abra o app **Arquivos** → **Downloads** → *frances-thais.apkg*).
3. Escolha **abrir com AnkiDroid** e toque em **Adicionar / OK**.

**Jeito 2 · pelo menu do AnkiDroid:**

1. Baixe o arquivo (passo 1 acima).
2. No AnkiDroid, na lista de decks, toque nos **⋮** (canto de cima, à direita).
3. Toque em **Importar** → **Pacote de deck** (*Deck package*) → escolha *frances-thais.apkg* em **Downloads**.

Pronto: aparece o deck **Francês da Thaís**, com as aulas dentro. 🎉

## 3️⃣ Ajustar: 10 cartões novos por dia

1. Na lista de decks, toque nos **⋮** ao lado de **Francês da Thaís** (ou segure o dedo no nome).
2. Toque em **Opções**.
3. Em **Novos cartões/dia**, ponha **10**. Salve.

Por que 10? Cada cartão novo volta várias vezes nos dias seguintes. Com 10 por dia, a revisão fica em **5–10 min**. Mais que isso vira bola de neve. ⛄

## 4️⃣ Como estudar

1. Toque em **Francês da Thaís** para estudar todas as aulas (ou numa aula específica).
2. Veja a frente. **Diga a resposta em voz alta** antes de virar. 🗣️
3. Toque em **Mostrar resposta** e ouça o áudio.
4. Seja honesta e escolha:

| Botão | Quando usar |
| --- | --- |
| 🔴 **Errei** (no app pode aparecer como *De novo* ou *Novamente*) | Não lembrei ou lembrei errado. Ele volta em minutos. |
| 🟠 **Difícil** | Lembrei, mas com muito esforço. |
| 🟢 **Bom** | Lembrei normal. **É o botão mais usado.** |
| 🔵 **Fácil** | Saiu na hora, sem pensar. Ele some por mais tempo. |

💡 Errar no Anki **não é ruim**: é o jeito de ele saber o que você precisa ver de novo.

## 5️⃣ Rotina diária (5–10 min) ⏱️

- **Um horário fixo:** no café da manhã, no metrô do Porto, na fila…
- **Primeiro as revisões**, depois os novos. O app já faz nessa ordem.
- **Fale em voz alta** e toque o áudio. Assim treina ouvido e pronúncia.
- **Não pule dias.** 5 min todo dia vale mais que 1 hora no domingo.
- Sem tempo? Faça só as revisões. Os novos podem esperar. 🌱

💡 Dá para fazer o Anki no **aquecimento de 5 min** das aulas. Conta como revisão espaçada! 🧠

## 6️⃣ Quando sair uma versão nova do deck 🔄

Quando entrarem aulas novas, o deck é atualizado aqui no site. Para receber **sem perder o progresso**:

1. Baixe de novo pelo mesmo link: **[frances-thais.apkg](https://tcandreetti.github.io/frances/anki/frances-thais.apkg)**.
2. Importe **por cima**, do mesmo jeito (passo 2). **Não apague** o deck antigo!
3. Se o app perguntar, mantenha **atualizar notas** e deixe **desmarcado** "importar progresso de estudo".

O que acontece:

- As palavras que você **já estuda** são reconhecidas (cada uma tem um código fixo) e **continuam com o seu progresso**.
- Só os cartões **novos** entram, nos subdecks das aulas novas.
- Correções de tradução ou de áudio nas palavras antigas também chegam. ✨
- ⚠️ Se uma frase **em francês** for corrigida, ela entra como cartão novo e a versão antiga **continua no seu celular**. Para apagar: toque na 🔍 (**Navegador**), procure a frase antiga, segure o dedo nela e escolha **Excluir nota**. Cada versão nova avisa aqui quais frases mudaram.

**Mudanças por versão:**

- **04/11/2026:** *J'habite à Lisbonne, au Portugal.* virou *J'habite à Porto, au Portugal.* (Aula 06). Se você importou antes, apague a frase com Lisbonne.

## 🛠️ Para quem mantém o curso

- Vocabulário: `scripts/anki_vocab.tsv` (aula · francês · português · áudio). Para uma aula nova, acrescente linhas.
- Gerar o deck: `python3 scripts/gerar_anki.py` (precisa de `genanki` e `edge-tts`). Sai em `docs/anki/frances-thais.apkg`.
- Áudio: usa o mp3 da aula com o mesmo texto; se não houver, gera com edge-tts e guarda em `scripts/anki_audio/`.
- IDs do modelo e dos decks são fixos, e o GUID de cada nota vem do texto em francês. **Não mude o texto em francês** de uma linha antiga (isso cria uma nota nova); corrija só o português.
