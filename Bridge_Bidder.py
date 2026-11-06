
import flet as ft
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

import json

firebase_json = json.loads(
    os.environ["FIREBASE_CREDENTIALS"]
)

cred = credentials.Certificate(firebase_json)


firebase_admin.initialize_app(cred)

db = firestore.client()

def load_game():
    return (
        db.collection("games")
        .document("table1")
        .get()
        .to_dict()
    )
def save_game(data):
    db.collection("games").document(
        "table1"
    ).set(
        data,
        merge=True
    )
def add_bid_to_firebase(player, bid):
    doc = db.collection("games").document("table1")

    data = doc.get().to_dict()

    auction = data.get("auction", [])

    auction.append(
        {
            "player": player,
            "bid": bid
        }
    )

    doc.update(
        {
            "auction": auction
        }
    ) 
def get_auction():
    data = load_game()
    return data.get("auction", [])     
def player_col(player):
    if player == "niki":
        return 0
    elif player == "tanya":
        return 1
    elif player == "nick":
        return 2
    elif player == "seb":
        return 3
 
def main(page):
    import threading
    import time
    my_player = None
    valid_calls = [
        "pass", "x", "xx",
        "1c","1d","1h","1s","1nt",
        "2c","2d","2h","2s","2nt",
        "3c","3d","3h","3s","3nt",
        "4c","4d","4h","4s","4nt",
        "5c","5d","5h","5s","5nt",
        "6c","6d","6h","6s","6nt",
        "7c","7d","7h","7s","7nt"
    ]
    game = load_game()

    turn = game.get("turn")

    print(game)
    saved_contract = game.get("contract", "")
    saved_declarer = game.get("declarer", "")
    saved_ttw = game.get("ttw", "")
    saved_tl = game.get("tl", "")


    contract = ft.Text(saved_contract)
    Ttw = ft.Text(saved_ttw)
    declarer = ft.Text(saved_declarer)
    Tl = ft.Text(saved_tl)
    isOpen = False
    NoP = 0

    def updater():
        nonlocal turn
        while True:
            game = load_game()
            

            turn = game.get("turn")
            bidBox.label = turn.capitalize()
            bidBox.update()
            rebuild_table()
            contract.value = game.get("contract", "")
            declarer.value = game.get("declarer", "")
            Ttw.value = game.get("ttw", "")
            Tl.value = game.get("tl", "")
            if contract.value != "":
                details.visible = True
            else:
                details.visible = False
            time.sleep(1)
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.WHITE
            headerSeb.color = ft.Colors.WHITE

            if turn == "niki":
                headerNiki.color = ft.Colors.AMBER
            elif turn == "tanya":
                headerTanya.color = ft.Colors.AMBER
            elif turn == "nick":
                headerNick.color = ft.Colors.AMBER
            elif turn == "seb":
                headerSeb.color = ft.Colors.AMBER
            page.update()
    def save_player(e):
        page.client_storage.set(
            "player",
            playerDropdown.value
        )
    def CLEAR(e):
        nonlocal row, turn, NoP, isOpen, headerSeb, headerNick, headerNiki, headerTanya

        passoutcheck.value = ""
          
        headerTanya.color = ft.Colors.WHITE
        headerNiki.color = ft.Colors.WHITE
        headerNick.color = ft.Colors.WHITE
        headerSeb.color = ft.Colors.WHITE
        if turn == "niki":
            headerNiki.color = ft.Colors.AMBER
        elif turn == "tanya":
            headerTanya.color = ft.Colors.AMBER
        elif turn == "nick":
            headerNick.color = ft.Colors.AMBER
        elif turn == "seb":
            headerSeb.color = ft.Colors.AMBER

        startingPlayer.value = ""

        row = 0
        turn = None
        NoP = 0
        isOpen = False
        save_game({
            "turn": "",
            "auction": [],
            "contract": "",
            "declarer": "",
            "ttw": "",
            "tl": ""
        })

        rebuild_table()

        contract.value = ""
        Ttw.value = ""
        Tl.value = ""
        declarer.value = ""

        details.visible = False

        startingPlayer.visible = True
        startingPlayerBttn.visible = True

        bidBox.visible = False
        bidBoxBttn.visible = False

        page.update()
    def inpStartingPlayer(e):
        nonlocal turn
        passoutcheck.value = ""
        startingPlayer.value = startingPlayer.value.lower().strip().replace(" ", "")

        if startingPlayer.value == "niki":
            turn = "niki"
            save_game({"turn": turn})
            
            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.AMBER
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.WHITE

            startingPlayer.visible = False
            startingPlayerBttn.visible = False
            bidBox.visible = True
            bidBoxBttn.visible = True
            page.update()
        elif startingPlayer.value == "tanya":
            turn = "tanya"
            save_game({"turn": turn})

            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.AMBER
            headerNick.color = ft.Colors.WHITE

            startingPlayer.visible = False
            startingPlayerBttn.visible = False
            bidBox.visible = True
            bidBoxBttn.visible = True
            page.update()
        elif startingPlayer.value == "nick":
            turn = "nick"
            save_game({"turn": turn})
            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.AMBER

            startingPlayer.visible = False
            startingPlayerBttn.visible = False
            bidBox.visible = True
            bidBoxBttn.visible = True
            page.update()
        elif startingPlayer.value == "seb" or startingPlayer.value == "sebastian":
            turn = "seb"
            
            save_game({"turn": turn})

            headerSeb.color = ft.Colors.AMBER
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.WHITE

            startingPlayer.visible = False
            startingPlayerBttn.visible = False
            bidBox.visible = True
            bidBoxBttn.visible = True
            page.update()
        else:
            passoutcheck.value = "INVALID DEALER"
            page.update()
            return
        bidBox.label = turn.capitalize()
        bidBox.update()
        
    def bid_value(bid):
        order = {
            "♣": 0,
            "♦": 1,
            "♥": 2,
            "♠": 3,
            "NT": 4
        }

        level = int(bid[0])

        if bid.endswith("NT"):
            strain = "NT"
        else:
            strain = bid[1]

        return (level - 1) * 5 + order[strain]
    def addRow():
        table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
        )
        page.update()
    def rebuild_table():

        table.rows.clear()

        auction = get_auction()

        current_row = [
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text(""))
        ]

        cells_used = 0

        for call in auction:

            col = player_col(call["player"])

            current_row[col] = ft.DataCell(
                ft.Text(call["bid"])
            )

            cells_used += 1

            if cells_used == 4:
                table.rows.append(
                    ft.DataRow(cells=current_row)
                )

                current_row = [
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(""))
                ]

                cells_used = 0

        if cells_used > 0:
            table.rows.append(
                ft.DataRow(cells=current_row)
            )

        page.update()
    row = 0
    prevBid = ""
    lastBid = ""

    cIsMentionedNN = False
    dIsMentionedNN = False
    hIsMentionedNN = False
    sIsMentionedNN = False
    ntIsMentionedNN = False

    cIsMentionedTS = False
    dIsMentionedTS = False
    hIsMentionedTS = False
    sIsMentionedTS = False
    ntIsMentionedTS = False
    fCNN = ""
    fDNN = ""
    fHNN = ""
    fSNN = ""
    fNTNN = ""
    fCTS = ""
    fDTS = ""
    fHTS = ""
    fSTS = ""
    fNTTS = ""

    LBP = None


    def bid(e):
        nonlocal my_player, turn, valid_calls, headerSeb, headerNick, headerNiki, headerTanya, Tl, row, turn, LBP, contract, Ttw, declarer, NoP, isOpen, prevBid, lastBid, cIsMentionedNN, dIsMentionedNN, hIsMentionedNN, sIsMentionedNN, ntIsMentionedNN, cIsMentionedTS, dIsMentionedTS, hIsMentionedTS, sIsMentionedTS, ntIsMentionedTS, fCNN, fDNN, fHNN, fSNN, fNTNN, fCTS, fDTS, fHTS, fSTS, fNTTS
        
        my_player = playerDropdown.value
        game = load_game()
        turn = game["turn"]
        
        if my_player != game["turn"]:
            passoutcheck.value = "NOT YOUR TURN"
            page.update()
            return
        bidBox.value = bidBox.value.lower().strip().replace(" ", "")
        if bidBox.value == "":
            passoutcheck.value = "ENTER A BID"
            page.update()
            return
        if bidBox.value not in valid_calls:
            passoutcheck.value = "INVALID CALL"
            page.update()
            return
        Fbid = None
        passoutcheck.value = ""
        if bidBox.value.endswith("c") or bidBox.value.endswith("d") or bidBox.value.endswith("h") or bidBox.value.endswith("s") or bidBox.value.endswith("nt") or bidBox.value == "x" or bidBox.value == "xx" or bidBox.value == "pass":
            if bidBox.value != "pass":
                isOpen = True
                NoP = 0
                if bidBox.value.startswith(("1", "2", "3", "4", "5", "6", "7")):
                    if turn == "niki" or turn == "nick":
                        LBP = "nn"
                    elif turn == "tanya" or turn == "seb":
                        LBP = "ts"

            if bidBox.value.startswith(("1", "2", "3", "4", "5", "6", "7")):
                if bidBox.value.endswith("nt"):
                    Fbid = bidBox.value[0] + "NT"
                    
                    if not ntIsMentionedNN and (turn == "niki" or turn == "nick"):
                        fNTNN = turn
                        ntIsMentionedNN = True
                    if not ntIsMentionedTS and (turn == "tanya" or turn == "seb"):
                        fNTTS = turn
                        ntIsMentionedTS = True
                elif bidBox.value.endswith("c"):
                    Fbid = bidBox.value[0] + "♣"
                    
                    if not cIsMentionedNN and (turn == "niki" or turn == "nick"):
                        fCNN = turn
                        cIsMentionedNN = True
                    if not cIsMentionedTS and (turn == "tanya" or turn == "seb"):
                        fCTS = turn
                        cIsMentionedTS = True
                elif bidBox.value.endswith("d"):
                    Fbid = bidBox.value[0] + "♦"
                    
                    if not dIsMentionedNN and (turn == "niki" or turn == "nick"):
                        fDNN = turn
                        dIsMentionedNN = True
                    if not cIsMentionedTS and (turn == "tanya" or turn == "seb"):
                        fCTS = turn
                        cIsMentionedTS = True
                elif bidBox.value.endswith("h"):
                    Fbid = bidBox.value[0] + "♥"
                    
                    if not hIsMentionedNN and (turn == "niki" or turn == "nick"):
                        fHNN = turn
                        hIsMentionedNN = True
                    if not hIsMentionedTS and (turn == "tanya" or turn == "seb"):
                        fHTS = turn
                        hIsMentionedTS = True
                elif bidBox.value.endswith("s"):
                    Fbid = bidBox.value[0] + "♠"
                    
                    if not sIsMentionedNN and (turn == "niki" or turn == "nick"):
                        fSNN = turn
                        sIsMentionedNN = True
                    if not hIsMentionedTS and (turn == "tanya" or turn == "seb"):
                        fHTS = turn
                        hIsMentionedTS = True
                
                if prevBid != "" and Fbid not in ["X", "XX", "/"]:
                    if bid_value(Fbid) <= bid_value(prevBid):
                        passoutcheck.value = "INSUFFICIENT BID"
                        page.update()
                        return
                prevBid = Fbid
                lastBid = Fbid
                add_bid_to_firebase(turn, Fbid)
                rebuild_table()
                auction = get_auction()

            elif bidBox.value == "x":
                Fbid = bidBox.value.upper()
                add_bid_to_firebase(turn, Fbid)
                rebuild_table()
                auction = get_auction()
            elif bidBox.value == "xx":
                Fbid = bidBox.value.upper()
                add_bid_to_firebase(turn, Fbid)
                rebuild_table()
                auction = get_auction()
                
            elif bidBox.value == "pass":
                Fbid = "/"
                NoP += 1
                add_bid_to_firebase(turn, Fbid)
                rebuild_table()
                auction = get_auction()
                if (len(auction) >= 4 and auction[-1]["bid"] == "/" and auction[-2]["bid"] == "/" and auction[-3]["bid"] == "/" and auction[-4]["bid"] == "/"):
                    #PASSOUT

                    headerTanya.color = ft.Colors.WHITE
                    headerNiki.color = ft.Colors.WHITE
                    headerNick.color = ft.Colors.WHITE
                    headerSeb.color = ft.Colors.WHITE

                    #contract.value = prevBid
                    #details.visible = True
                    bidBox.visible = False
                    bidBoxBttn.visible = False
                    #if LBP == "nn":
                        #if prevBid.endswith("♥"):
                            #declarer.value = fHNN.upper()
                        #elif prevBid.endswith("♣"):
                            #declarer.value = fCNN.upper()
                        #elif prevBid.endswith("♦"):
                            #declarer.value = fDNN.upper()
                        #elif prevBid.endswith("♠"):
                            #declarer.value = fSNN.upper()
                        #elif prevBid.endswith("NT"):
                            #declarer.value = fNTNN.upper()
                    #elif LBP == "ts":
                        #if prevBid.endswith("♥"):
                            #declarer.value = fHTS.upper()
                        #elif prevBid.endswith("♣"):
                            #declarer.value = fCTS.upper()
                        #elif prevBid.endswith("♦"):
                            #declarer.value = fDTS.upper()
                        #elif prevBid.endswith("♠"):
                            #declarer.value = fSTS.upper()
                        #elif prevBid.endswith("NT"):
                            #declarer.value = fNTTS.upper()
                    passoutcheck.value = "PASSED OUT"
                    page.update()
                    return
                if (len(auction) >= 4 and auction[-1]["bid"] == "/" and auction[-2]["bid"] == "/" and auction[-3]["bid"] == "/" and auction[-4]["bid"] != "/"):
                    
                    
                    
                    
                    
                    contract_bid = ""

                    for call in reversed(auction):
                        bid = call["bid"]

                        if (
                            bid.endswith("♣")
                            or bid.endswith("♦")
                            or bid.endswith("♥")
                            or bid.endswith("♠")
                            or bid.endswith("NT")
                        ):
                            contract_bid = bid
                            break

                    #BIDDING NATURALLY CLOSED

                    headerTanya.color = ft.Colors.WHITE
                    headerNiki.color = ft.Colors.WHITE
                    headerNick.color = ft.Colors.WHITE
                    headerSeb.color = ft.Colors.WHITE

                    details.visible = True
                    bidBox.visible = False
                    bidBoxBttn.visible = False
                    contract.value = contract_bid
                    prevbval = int(contract_bid[0]) + 6
                    TlP = 14 - prevbval
                    Tl.value = str(TlP)
                    Ttw.value = str(prevbval)
                    save_game({
                        "contract": contract.value,
                        "declarer": declarer.value,
                        "ttw": Ttw.value,
                        "tl": Tl.value
                    })
                    winning_side = None

                    for call in reversed(auction):
                        bid = call["bid"]

                        if (
                            bid.endswith("♣")
                            or bid.endswith("♦")
                            or bid.endswith("♥")
                            or bid.endswith("♠")
                            or bid.endswith("NT")
                        ):
                            bidder = call["player"]

                            if bidder in ["niki", "nick"]:
                                winning_side = ["niki", "nick"]
                            else:
                                winning_side = ["tanya", "seb"]

                            break

                    strain = contract_bid[1:]

                    for call in auction:
                        bidder = call["player"]
                        bid = call["bid"]

                        if bidder not in winning_side:
                            continue

                        if bid.endswith(strain):
                            declarer.value = bidder
                            break
                    print("contract_bid =", contract_bid)
                    print("LBP =", repr(LBP))

                    print("fCNN =", repr(fCNN))
                    print("fDNN =", repr(fDNN))
                    print("fHNN =", repr(fHNN))
                    print("fSNN =", repr(fSNN))
                    print("fNTNN =", repr(fNTNN))

                    print("fCTS =", repr(fCTS))
                    print("fDTS =", repr(fDTS))
                    print("fHTS =", repr(fHTS))
                    print("fSTS =", repr(fSTS))
                    print("fNTTS =", repr(fNTTS))

                    print("declarer before save =", repr(declarer.value))

                    save_game({
                        "contract": contract.value,
                        "declarer": declarer.value,
                        "ttw": Ttw.value,
                        "tl": Tl.value
                    })
                    page.update()
                    return
                    
                page.update()
                

            
            
            col = 0
            if turn == "seb":
                col = 3
            elif turn == "niki":
                col = 0
            elif turn == "tanya":
                col = 1
            elif turn == "nick":
                col = 2
        if turn == "seb":
            table.rows[row].cells[col].content.value = Fbid
            row += 1
            addRow()
            
            turn = "niki"
            save_game({"turn": turn})
            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.AMBER
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.WHITE
            bidBox.label = turn
            page.update()
        elif turn == "niki":
            table.rows[row].cells[col].content.value = Fbid
            turn = "tanya"
            save_game({"turn": turn})
            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.AMBER
            headerNick.color = ft.Colors.WHITE
            bidBox.label = turn
            page.update()
        elif turn == "tanya":
            table.rows[row].cells[col].content.value = Fbid
            turn = "nick"
            save_game({"turn": turn})
            headerSeb.color = ft.Colors.WHITE
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.AMBER
            bidBox.label = turn
            page.update()
        elif turn == "nick":
            table.rows[row].cells[col].content.value = Fbid
            turn = "seb"
            save_game({"turn": turn})
            headerSeb.color = ft.Colors.AMBER
            headerNiki.color = ft.Colors.WHITE
            headerTanya.color = ft.Colors.WHITE
            headerNick.color = ft.Colors.WHITE
            bidBox.label = turn
            page.update()
        bidBox.value = ""
        page.update()



        



    startingPlayer = ft.TextField(label="Dealer", on_submit=inpStartingPlayer)
    startingPlayerBttn = ft.Button(content=ft.Text("Submit"), on_click=inpStartingPlayer)
    restartBttn = ft.Button(content=ft.Text("CLEAR"), on_long_press=CLEAR)
    passoutcheck = ft.Text(color=ft.Colors.RED_ACCENT)
    playerDropdown = ft.Dropdown(
        label="Who am I?",
        options=[
            ft.dropdown.Option("niki"),
            ft.dropdown.Option("tanya"),
            ft.dropdown.Option("nick"),
            ft.dropdown.Option("seb"),
        ],
        
    )


    headerNiki = ft.Text("Niki", color=ft.Colors.WHITE)
    headerTanya = ft.Text("Tanya", color=ft.Colors.WHITE)
    headerNick = ft.Text("Nick", color=ft.Colors.WHITE)
    headerSeb = ft.Text("Seb", color=ft.Colors.WHITE)
    table = ft.DataTable(
        columns=[
            ft.DataColumn(headerNiki),
            ft.DataColumn(headerTanya),
            ft.DataColumn(headerNick),
            ft.DataColumn(headerSeb)
        ]
    
    

        
    )
    rebuild_table()

    details = ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("CONTRACT")),
            ft.DataColumn(ft.Text("TTW")),
            ft.DataColumn(ft.Text("TL")),
            ft.DataColumn(ft.Text("DECL."))
            
        ]
    )
    details.visible = False
    
    details.rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(contract),
                ft.DataCell(Ttw),
                ft.DataCell(Tl),
                ft.DataCell(declarer)

            ]
        )
    )
    page.update()

    bidBox = ft.TextField(label=turn, on_submit=bid)
    bidBoxBttn = ft.Button(content=ft.Text("Bid"), on_click=bid)
    bidBox.visible = False
    bidBoxBttn.visible = False

    

    
    page.add(playerDropdown, ft.Row([startingPlayer, startingPlayerBttn]), ft.Row([bidBox, bidBoxBttn]), ft.Row([table, details]), passoutcheck, restartBttn)
    threading.Thread(
        target=updater,
        daemon=True
    ).start()
ft.run(main)



