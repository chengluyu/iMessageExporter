import sqlite3
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from datetime import date
from optparse import OptionParser
    

if __name__ == '__main__':
    opt = OptionParser(usage='%prog [TEST-SPECS]')
    opt.add_option('-d', '--database', dest='database', action='store',
                   help='Specify the path to the database')

    (options, args) = opt.parse_args()

    conn = sqlite3.connect(options.database)
    c = conn.cursor()

    c.execute('SELECT * FROM chat')
    all_chat_rows = c.fetchall()

    data = []
    
    for chat_row in all_chat_rows:
        chat_id = chat_row[0]
        
        c.execute("SELECT 978307200 + m.date, COUNT(*) FROM message m INNER JOIN chat_message_join c ON m.ROWID = c.message_id WHERE c.chat_id = ? GROUP BY date(978307200 + m.date, 'unixepoch')", (chat_id, ))
        messages = c.fetchall()

        xs = list(map(lambda row: date.fromtimestamp(row[0]), messages))
        ys = list(map(lambda row: row[1], messages))
        name = chat_row[6]

        data.append((xs, ys, name, sum(ys)))
    
    data.sort(key=lambda x: x[3])
    data.reverse()
    data = data[:10]

    rects = []

    fig, ax = plt.subplots()

    for xs, ys, name, total in data:
        bar_container = ax.bar(xs, ys)
        rects.append(bar_container[0])
        print(name, total)
        
    ax.xaxis_date()
    ax.legend(rects, list(map(lambda x: x[2], data)))
    plt.show()
