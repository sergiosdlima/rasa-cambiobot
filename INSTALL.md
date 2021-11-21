# Intalação e preparação do ambiente

1. Criei um ambiente virtual utilizando o Python 3.6, 3.7 ou 3.8 para isolar as dependências do Rasa.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale o rasa, o componente spacynlp e o modelo spacy pre-treinado em ptbr:

```bash
pip install rasa[spacy]
python -m spacy download
```

Obs: Pode ser necessário atualizar o spacy (`pip install -U spacy`) para a compatibilidade com o modelo PT-BR.
Obs2: Baixar no mínimo o medelo médio pt_core_news_md para treinar. Preferencialmente baixe o modelo grande pt_core_news_lg.

3. Pronto!