# Simulatore di sistemi elettorali

Framework per l'elaborazione di sistemi elettorali

## Modo d'uso

Installare le dipendenze con
```shell script
pip install -r requirements.txt
```


Creare una cartella in Electoral Laws/nome_legge con la seguente struttura:
+ Data
+ Instances
+ Classes

si vedano le cartelle di documentazione per informazioni su cosa vada inserito
in queste cartelle.

Eseguire in questa cartella:

```shell script
python -m src /path/to/folder_nome_legge
```
o in una console python:

```python
import src
src.run_simulation("/path/to/folder")
```

## Esempio

`LeggiElettorali` contiene tre configurazioni per simulare le elezioni europee in Italia
del 2019, l'elezione della Camera dei Deputati del 2013 con l'utilizzo della Legge Calderoli 
e l'elezione della Camera dei Deputati del 2001 con la legge Mattarella.
