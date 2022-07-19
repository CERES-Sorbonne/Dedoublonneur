from glob import glob
from typing import List, Optional, Tuple

import json
import os
import pickle
import typer

from dedoubloneur import avance


def save_object(obj, filename):
    with open(f"res/{filename}", 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def open_object(filename):
    with open(f"res/{filename}", 'rb') as inp:
        return pickle.load(inp)


def export(obj, filename, mode=("indexD",)):
    lsreturn = []

    if "indexD" in mode:
        lsdoublons = (str(e) for e in obj.index_doublons)
        idb = "<IndexDoublons>" + ";".join(lsdoublons) + "</IndexDoublons>"
        lsreturn.append(idb)

    with open(f"'{filename}'result.txt", mode='w', encoding="utf-8") as f:
        f.write('\n'.join(lsreturn))


os.makedirs("res/", exist_ok=True)

i = len((glob("res/instance*.pkl")))
print(i)

app = typer.Typer()
fichier = {"path": None,
           "data": None,
           "instance": None,
           "res": None
           }

config_params = {"nombre_pivots": 0,
                 "taille_des_groupes": 0,
                 "sensibilite": 0}


@app.callback(invoke_without_command=True)
def init(liste_fic: str = typer.Option(...)):
    if os.path.exists("cli.json"):
        with open("cli.json", mode="r", encoding="utf-8") as j:
            config_file = json.load(j)
        typer.echo("config loaded from cli.json")
    else:
        config_file = {"nombre_pivots": 50,
                       "taille_des_groupes": 1000,
                       "sensibilite": 0.00001}

        with open("cli.json", mode="w", encoding="utf-8") as j:
            json.dump(config_file, j, indent=2)
        typer.echo("config saved to cli.json")

    for key, val in config_file.items():
        config_params[key] = val

    with open(liste_fic, 'rb') as fp:
        list_to_process = pickle.load(fp)

    if os.path.exists(f"{liste_fic}.json"):
        with open(f"{liste_fic}.json", mode="r", encoding="utf-8") as j:
            fichier_ = json.load(j)

        for key, val in fichier_.items():
            fichier[key] = val

        fichier["path"] = liste_fic
        fichier["data"] = list_to_process

    with open(f"{liste_fic}.json", mode="w", encoding="utf-8") as j:
        json.dump(fichier, j, indent=2)
    typer.echo(f"\nfile params saved to {liste_fic}.json")


@app.command()
def change_config(key: Optional[List[str]] = typer.Option(None),
                  value: Optional[List[int]] = typer.Option(None)):
    if not (key or value):
        typer.launch("cli.json")
        typer.echo("No options passed, opening the config file")
        raise typer.Exit()

    for k, v in zip(key, value):
        config_params[k] = v

    with open("cli.json", mode="w", encoding="utf-8") as j:
        json.dump(config_params, j, indent=2)
    typer.echo("config saved to cli.json")


@app.command()
def load():
    if fichier["instance"] is not None:
        typer.confirm("There already is an instance for this list do you want to overwrite it ?", abort=True)
    instance = avance.Avance(fichier["data"], nb_pivots=40)
    save_object(instance, f"instance{i}.pkl")
    fichier["instance"] = f"instance{i}.pkl"

    liste_fic = fichier["path"]

    with open(f"{liste_fic}.json", mode="w", encoding="utf-8") as j:
        json.dump(fichier, j, indent=2)
    typer.echo(f"\nfile params saved to {liste_fic}.json")


@app.command()
def process():
    if fichier["res"] is not None:
        typer.confirm("There already is a processed version of this list do you want to overwrite it ?", abort=True)

    instance = open_object(fichier["instance"])

    instance.process(taillegroupe=50, sensibilite=.0004)

    save_object(fichier["instance"], f"instance{i}.pkl")

    fichier["res"] = f"instance{i}.pkl"

    liste_fic = fichier["path"]

    with open(f"{liste_fic}.json", mode="w", encoding="utf-8") as j:
        json.dump(fichier, j, indent=2)
    typer.echo(f"\nfile params saved to {liste_fic}.json")

    export(instance, liste_fic)


@app.command()
def total():
    instance = avance.Avance(fichier["data"], nb_pivots=40)
    instance.process(taillegroupe=50, sensibilite=.0004)
    save_object(instance, f"instance{i}.pkl")
    fichier["instance"] = f"instance{i}.pkl"
    fichier["res"] = f"instance{i}.pkl"

    liste_fic = fichier["path"]

    with open(f"{liste_fic}.json", mode="w", encoding="utf-8") as j:
        json.dump(fichier, j, indent=2)
    typer.echo(f"\nfile params saved to {liste_fic}.json")

    export(instance, liste_fic)


if __name__ == "__main__":
    app()
