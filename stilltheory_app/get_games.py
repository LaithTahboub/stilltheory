import re
import urllib
import urllib.request
import psycopg2
import sys
import chess
import time

# Section 1: Obtain games
def prepare_database(usr, usr_id):
    account = 'l'
    username = usr  
    opening = ""
    color = ""
    num_games_to_analyze = 500
    conn = psycopg2.connect(
        user="postgres",
        host="127.0.0.1",
        port="5432",
        database="stilltheory_database",
        password="tahboub989" 
    )
    cursor = conn.cursor()

    # url = "https://lichess.org/api/games/user/" + username + "?opening=true"
    # pgn = urllib.request.urlopen(url)
    # game_info = ""
    # counter = 0
    # moves = []
    # moves.append("")
    # cnt = 0
    # result_list = []
    # game_id_list = []
    # variant_list = []
    # color_list = []
    # for line in pgn: 
    #     curr = (line.decode('utf-8'))
    #     game_info += curr
    #     if "Event " in curr:
    #         if counter == num_games_to_analyze + 1:
    #             break
    #         counter += 1
    #     if "Site " in curr:
    #         game_id_list.append(curr[26:len(curr) - 2])
    #     if ("White " in curr) and (curr.lower() == '[white "' + username + '"]\n'):
    #         color = "white" 
    #         color_list.append(color)
    #     elif ("White " in curr):
    #         # print('[White "' + username + '"]\n' + curr)
    #         color = "black" 
    #         color_list.append(color)
    #     # if ("Black " in curr) and (curr == ("[Black \"" + username + "\"]\n")):
    #     #     color = "black"
    #     #     color_list.append(color)
    #     # elif ("Black " in curr):
    #     #     print(curr)
        
    #     if "Result " in curr and curr == "[Result \"1/2-1/2\"]\n":
    #         result = "draw"
    #         result_list.append(result)
    #     elif "Result " in curr and (curr == "[Result \"1-0\"]\n" and color == "white"):
    #         result = "win"
    #         result_list.append(result)
    #     elif "Result " in curr and (curr == "[Result \"1-0\"]\n" and color == "black"):
    #         result = "loss"
    #         result_list.append(result)
    #     elif "Result " in curr and (curr == "[Result \"0-1\"]\n" and color == "white"):
    #         result = "loss"
    #         result_list.append(result)
    #     elif "Result " in curr and (curr == "[Result \"0-1\"]\n" and color == "black"):
    #         result = "win"
    #         result_list.append(result)
    #     if "Opening " in curr:
    #         start = curr.index('\"') + 1
    #         opening = curr[start:len(curr) - 3]
    #         # print(opening + '\n')
    #     if "Variant " in curr:
    #         start = curr.index('\"') + 1
    #         variant = curr[start:len(curr) - 3]
    #         variant_list.append(variant)
    #     if ("1-0" in curr or "0-1" in curr or "1/2-1/2" in curr) and "Result " not in curr:
    #         moves[cnt] += curr
    #         moves.append("")
    #         cnt += 1


    #     # if "Event " not in curr and "Site" not in curr and "Date" not in curr and "White" not in curr and "Black " not in curr and "Result " not in curr and "UTCDate" not in curr and "UTCTime" not in curr and "WhiteElo" not in curr and "BlackElo" not in curr and "WhiteRatingDiff " not in curr and "BlackRatingDiff" not in curr and "Variant " not in curr and "TimeControl " not in curr and "ECO " not in curr and "Opening " not in curr and "Termination " not in curr:
    #     #     moves[cnt] += curr 

    # #-------------------------------------------------------------------------------------------------------------------------------# Section 2: Generate tree


    # #the move_list contains every move in every game. the position_list contains every position in every game. the position_uci_list contains every position in uci format in every game. the variation_list contains the name of every variation reached in every game.
    # # TODO: look into fen, might be faster
    # moves.remove("")
    user_id = usr_id
    # move_list = [[]] 
    # position_list = [[[]]]
    # position_uci_list = [[[]]]
    # variation_list = [[[]]]


    # # print(game_id_list)

    # # print games
    # # for game in moves:
    # #     print(game)

    # # cut result from games

    # for i in range(0, len(moves)):
    #     moves[i] = moves[i][0:len(moves[i]) - 1]
    #     # print(len(game))
    #     if moves[i][len(moves[i]) - 1] == '2':
    #         moves[i] = moves[i][0:len(moves[i]) - 7]
    #     else:
    #         moves[i] = moves[i][0:len(moves[i]) - 3]
    #     moves[i] = moves[i].split()
    #     del(moves[i][::3])
    #     moves[i] = " ".join(moves[i])
    #     # #todo: check checkmate
    #     move_list.append(moves[i].split())
    #     # move_list[i] = move_list[i][:-1]
    # #(move_list)

    # uci_moves = [[]]
    # fen_list = [[]]
    # x = 0
    # for game in move_list:
    #     board = chess.Board()
    #     uci_moves.append([])
    #     fen_list.append([])
    #     for move in game:
    #         # print(move)
    #         uci_moves[x].append(board.push_san(move).uci())
    #         fen_list[x].append(board.fen())
    #         # board.parse_uci(board.push_san(move).uci())

    #     x += 1
    # del(fen_list[0])
    # del(fen_list[-1])

    # for i in range(0, len(move_list)):
    #     position_list.append([])
    #     position_uci_list.append([])
    #     variant_list.append([])
    #     curr = ""
    #     curr_uci = ""
    #     for j in range(0, len(move_list[i])):
    #         curr += move_list[i][j] + ' '
    #         curr_uci += uci_moves[i][j] + ' '
    #         position_list[i].append(curr[:-1])
    #         position_uci_list[i].append(curr_uci[:-1])
    #         # opening processing:
    #         #   url2) 
    #         # opening_info = urllib.request.urlopen(url2)
    #         # for line in opening_info: 
    #         #     curr_line = (line.decode('utf-8'))
    #         #     if "opening" in curr_line:
    #         #         print(curr_line)
    # # url2 = 'https://explorer.lichess.ovh/masters?play=d2d4'   
    # # opening_info = urllib.request.urlopen(url2)
    


    # # TODO: fix following lines: shouldn't be necessary to delete first and last, but for some reason extraneous elements are being added
    # del(position_list[0])
    # del(position_list[-1])


    # del(position_uci_list[0])
    # del(position_uci_list[-1])

    # del(variant_list[0])
    # del(variant_list[-1])

    # # print(position_uci_list)
    # move_list = move_list[1:]

    

    # print(str(len(color_list)) + ' ' + str(len(game_id_list)))
    # # tenemos todo lo que necesitamos en este punto
    # result_and_game_id_and_position_and_color_and_variant_index = 0
    # for game in move_list:
    #     if variant_list[result_and_game_id_and_position_and_color_and_variant_index] == 'Standard':
    #         for i in range(0, min(len(game), 15)):
    #                 if result_list[result_and_game_id_and_position_and_color_and_variant_index] == 'win':
    #                     cursor.execute("""
    #                     INSERT INTO moves(move, color, win, loss, draw, game_id, sequence, position, user_id, uci_position, fen_position) VALUES('%s', '%s', TRUE, FALSE, FALSE, '%s', '%s', '%s', '%s', '%s', '%s')
    #                     """ % (game[i], color_list[result_and_game_id_and_position_and_color_and_variant_index], game_id_list[result_and_game_id_and_position_and_color_and_variant_index], i + 1, position_list[result_and_game_id_and_position_and_color_and_variant_index][i], user_id, position_uci_list[result_and_game_id_and_position_and_color_and_variant_index][i], fen_list[result_and_game_id_and_position_and_color_and_variant_index][i]))
    #                     conn.commit()
    #                 elif result_list[result_and_game_id_and_position_and_color_and_variant_index] == 'loss':
    #                     cursor.execute("""
    #                     INSERT INTO moves(move, color, win, loss, draw, game_id, sequence, position, user_id, uci_position, fen_position) VALUES('%s', '%s', FALSE, TRUE, FALSE, '%s', '%s', '%s', '%s', '%s', '%s')
    #                     """ % (game[i], color_list[result_and_game_id_and_position_and_color_and_variant_index], game_id_list[result_and_game_id_and_position_and_color_and_variant_index], i + 1, position_list[result_and_game_id_and_position_and_color_and_variant_index][i], user_id, position_uci_list[result_and_game_id_and_position_and_color_and_variant_index][i], fen_list[result_and_game_id_and_position_and_color_and_variant_index][i]))
    #                     conn.commit()
    #                 else:
    #                     cursor.execute("""
    #                     INSERT INTO moves(move, color, win, loss, draw, game_id, sequence, position, user_id, uci_position, fen_position) VALUES('%s', '%s', FALSE, FALSE, TRUE, '%s', '%s', '%s', '%s', '%s', '%s')
    #                     """ % (game[i], color_list[result_and_game_id_and_position_and_color_and_variant_index], game_id_list[result_and_game_id_and_position_and_color_and_variant_index], i + 1, position_list[result_and_game_id_and_position_and_color_and_variant_index][i], user_id, position_uci_list[result_and_game_id_and_position_and_color_and_variant_index][i], fen_list[result_and_game_id_and_position_and_color_and_variant_index][i]))
    #                     conn.commit()
    #     result_and_game_id_and_position_and_color_and_variant_index += 1

    cursor.execute("""
    TRUNCATE TABLE opening_tree RESTART IDENTITY;
    """)
    conn.commit()
    cursor1 = conn.cursor()

    cursor1.execute("""
    SELECT id, uci_position
    FROM moves
    WHERE opening is null AND user_id = '%s'
    """ % (user_id,))
    # print(cursor.rowcount)
    sleepCnt = 0
    for record in cursor1:
        # check if look up table has opening
        cursor2 = conn.cursor()
        cursor2.execute("""
        SELECT opening_variation_name
        FROM opening_variation_look_up
        WHERE opening_variation_position = '%s'
        """ % (record[1],))
        opening = ''
        if cursor2.rowcount == 0:
        # get opening name:
            url2 = 'https://explorer.lichess.ovh/masters?play=' + ','.join(record[1].split())   
            try:
                info =  urllib.request.urlopen(url2)
            except:
                time.sleep(3)
                info =  urllib.request.urlopen(url2)

            for line in info:
                curr_line = (line.decode('utf-8'))
                for i in range(0, len(curr_line) - 6):
                    if curr_line[i] == 'o' and curr_line[i + 1] == 'p' and curr_line[i + 2] == 'e' and curr_line[i + 3] == 'n' and curr_line[i + 4] == 'i' and curr_line[i + 5] == 'n' and curr_line[i + 6] == 'g':
                        opening = curr_line[i:]
            indexOfStart = opening.index('name')
            indexOfStart += 7
            opening = opening[indexOfStart:]
            indexOfEnd = opening.index('\"')
            opening = opening[:indexOfEnd]       
            # check for apostrophes
            opening = fix_apostrophe_for_sql(opening)
            # print('opening:' +opening)
                        
        # insert opening in look up table and update moves:
            cursor3 = conn.cursor()
            cursor3.execute("""
            INSERT INTO opening_variation_look_up(opening_variation_position, opening_variation_name)
            VALUES('%s', '%s')
            """ % (record[1],opening))
            conn.commit()
        else:
            cursor4 = conn.cursor()
            cursor4.execute("""
            SELECT opening_variation_name
            FROM opening_variation_look_up  
            WHERE opening_variation_position = '%s'
            """ % (record[1],))
            opening = cursor4.fetchone()
            opening = opening[0]
            opening = fix_apostrophe_for_sql(opening)
            # print('opening exists in look up table' + str(record[1]) + opening)
        cursor5 = conn.cursor()
        # print(opening)
        cursor5.execute("""
        UPDATE moves
        SET opening = '%s'
        WHERE id = '%s' AND user_id = '%s'
        """ % (opening, record[0], usr_id))
        conn.commit()

# populate opening_tree
    cursor6 = conn.cursor()
    cursor6.execute("""
    INSERT INTO opening_tree(sequence, position, color, num_games, num_wins, num_losses, num_draws, user_id, fen_position) 
    SELECT moves.sequence, moves.position, moves.color, COUNT(*), 
    SUM(CASE WHEN win = TRUE THEN 1 ELSE 0 END), 
    SUM(CASE WHEN loss = TRUE THEN 1 ELSE 0 END),
    SUM(CASE WHEN draw = TRUE THEN 1 ELSE 0 END),
    user_id, fen_position
    FROM moves
    GROUP BY sequence, position, color, user_id, fen_position
    """)
    conn.commit()

    cursorxy = conn.cursor()
    cursorxy.execute(
        """
        DELETE from opening_tree WHERE num_games < 5
        """
    )

# get parent id:
    cursor7 = conn.cursor()
    cursor7.execute("""
    UPDATE opening_tree AS co
    SET parent_id = 
    (SELECT po.id
       FROM opening_tree AS po
       WHERE po.position = SUBSTRING(co.position, 0, (LENGTH(co.position) - STRPOS(REVERSE(co.position), ' ') + 1 )) 
	   AND po.user_id = co.user_id 
	   AND po.color = co.color
       LIMIT 1)
    WHERE co.sequence > 1
    """)
    conn.commit()

# merge logic:
    for i in range(14, 0, -1):
        cursor8 = conn.cursor()
        cursor8.execute(
            """
            SELECT parent.id, (
                SELECT COUNT(child.id)
                FROM opening_tree AS child
                WHERE child.parent_id = parent.id
            )
            FROM opening_tree AS parent
            WHERE parent.sequence = '%s' 
            """ % (i,)
        )
        # print('dasdasdsa')
        for record in cursor8:
            if record[1] == 1:
                cursor9 = conn.cursor()
                cursor9.execute(
                    """
                    SELECT position, id, fen_position
                    FROM opening_tree 
                    WHERE parent_id = '%s' AND user_id = '%s'
                    """ % (record[0], usr_id)
                )
                conn.commit()

                child_record = cursor9.fetchone()
                cursor10 = conn.cursor()
                cursor10.execute(
                        """
                        DELETE FROM opening_tree
                        WHERE sequence = '%s' AND parent_id = '%s' AND user_id = '%s'
                        """ % (i + 1, record[0], usr_id)
                    )
                conn.commit()
                
                cursor11 = conn.cursor()
                cursor11.execute(
                    """
                    UPDATE opening_tree
                    SET position = '%s', fen_position = '%s'
                    WHERE sequence = '%s' AND id = '%s' AND user_id = '%s'
                    """ % (child_record[0], child_record[2], i, record[0], usr_id)
                )
                conn.commit()

                cursor12 = conn.cursor()
                cursor12.execute(
                    """
                    UPDATE opening_tree
                    SET parent_id = '%s'
                    WHERE parent_id = '%s' AND user_id = '%s'
                    """ % (record[0], child_record[1], user_id)
                )
                conn.commit()

    cursorx = conn.cursor()
    cursorx.execute(
        """
        SELECT id, position
        FROM opening_tree 
        WHERE user_id = '%s'
        """ % (usr_id,)
    )
    for record in cursorx:
        cursory = conn.cursor()
        cursory.execute(
            """
            UPDATE opening_tree
            SET opening_variation = (
                SELECT opening
                FROM moves
                WHERE moves.position = '%s' AND user_id = '%s'
                LIMIT 1
            )
            WHERE id = '%s'
            """ % (record[1], usr_id, record[0])
        )

        conn.commit()














# *chess.com logic--to be added later:

# if account == 'c':
#     baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
#     archivesUrl = baseUrl + "archives"

#     #read the archives url and store in a list
#     file = urllib.request.urlopen(archivesUrl)
#     archives = file.read().decode("utf-8")
#     archives = archives.replace("{\"archives\":[\"", "\",\"")
#     archivesList = archives.split("\",\"" + baseUrl)
#     archivesList[len(archivesList)-1] = archivesList[len(archivesList)-1].rstrip("\"]}")

#     #download all the archives
#     for i in range(len(archivesList)-1):
#         url = baseUrl + archivesList[i+1] + "/pgn"
#         filename = archivesList[i+1].replace("/", "-")
#         urllib.request.urlretrieve(url, "/Users/laithtahboub/Desktop/Chess Games/" + filename + ".pgn") #change
#         print(filename + ".pgn has been downloaded.")
#     print ("All files have been downloaded.")

# else:
# def prepare_opening_variation_look_up_table():

def fix_apostrophe_for_sql(string):
    # for i in range(1, len(string)):
    #     if string[i] == '\'':
    #         string = string[:i] + "'" + string[i:]
    #         # dadsadas'sdsadasda'
    #         # dadsadas''sdsadasda' 

    #         i += 4
    string = string.replace('\'', '\'\'')

    return string