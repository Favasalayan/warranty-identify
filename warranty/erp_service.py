from datetime import date

from dateutil.relativedelta import relativedelta
from .erp_connection import get_erp_connection


def get_warranty_items(invoice):

    conn = get_erp_connection()

    cursor = conn.cursor()

    query = """
    SELECT
    t.[Receipt No_],
    t.[Item No_],
    t.[Date],
    i.[Description],
    i.[Description 2],
    i.[Service Duration(Month)],
    i.[Service Team Name],
    i.[Salesman Name],
    i.[Salesman Mobile],
    i.[Vendor No_]

    FROM
    (
    SELECT
    [Receipt No_],
    [Item No_],
    [Date]
    FROM [House Care Live$Trans_ Sales Entry] WITH (NOLOCK)
    WHERE [Receipt No_] = ?
    ) t

    JOIN [House Care Live$Item] i WITH (NOLOCK)
    ON t.[Item No_] = i.[No_]

    WHERE i.[Warranty Card] = 1
    """

    cursor.execute(query, invoice)

    rows = cursor.fetchall()

    items = []

    for r in rows:

        purchase = r[2]

        months = r[5] or 0

        expiry = purchase + relativedelta(months=months)
            
        items.append({

            "item_no": r[1],

            "item": r[3],

            "item_ar": r[4],

            "purchase": purchase.strftime("%d-%m-%Y"),

            "expiry": expiry.strftime("%d-%m-%Y"),

            "warranty_months": months,

            "warranty_provider": r[6],

            "salesman": r[7],

            "phone": r[8],
            
            "vendor_no": r[9]

        })

    cursor.close()

    conn.close()

    return items

