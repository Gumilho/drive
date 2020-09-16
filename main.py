import datetime
from trello import TrelloClient
import pathlib
import os
from Secret import api_key, api_secret, token


def find(iterable, name):
    return next((x for x in iterable if x.name == name), None)


if __name__ == '__main__':

    client = TrelloClient(api_key=api_key, api_secret=api_secret, token=token)
    board = find(client.list_boards(), 'Quadro Teste')
    labels = board.get_labels()
    label_avail = find(labels, "Disponível")
    label_unavail = find(labels, "Indisponível")
    lists = board.list_lists()
    for tlist in lists:
        if tlist.name == "Omotenashi":
            continue
        chapter_list = {}

        for card in tlist
