# Método Simplex em python

Código em python do método simplex para busca operacional na forma padrão para a matéria de programação linear do IPRJ ( Instituto Politécnico do Rio de Janeiro )

## Uso

```
I - git clone https://github.com/joaovitor32/simplex-py
II - cd ./simplex-py
III - pip3 install -r requirements.txt
IV - python3 -B ./src/main.py
```

## Importante
```
É necessário popular o arquivo simplex.yaml da seguinte 
  Z  |  x1  |   ....   |    xf2   |    xf3    |      b   
 --- | ---- |  ------  |  ------- | --------- |   --------
  v1 |  v5  |    ...   |    v9    |    v13    |     v17 
  v2 |  v6  |    ...   |    v10   |    v14    |     v18 
  v3 |  v7  |    ...   |    v11   |    v15    |     v19 
  v4 |  v8  |    ...   |    v12   |    v16    |     v20 

* É necessário editar simplex.yaml para setar variáveis de ambiente específicas

** Vi são valores relacionados a restrição ou relativos

*** A tabela acima é modificada na hora de plotar a região factível,
nesse momento as variáveis livres adicionadas são desconsideradas.

```
## Passos

```
1 passo - identificar variável que entra
2 passo - identificar linha que sai   
3 passo - identificar o elemento pivot
4 passo - calcular a nova linha pivot
5 passo - calcular as novas matrizes
``` 

## To execute tests

```
I - python3 -B ./src/__tests__/simplex.py 
```


## Reference

```
I - stack overflow: https://stackoverflow.com/questions/65343771/solve-linear-inequalities
II - link: https://geekrodion.com/blog/operations/simplex
```
