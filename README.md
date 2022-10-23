# origins-market-tracker

Tools used:  Python/Flask, PostgreSQL, SQLAlchemy, Jinja, API, HTML, CSS

** NOTE **
Unfortunately, the game private server has been closed, meaning no more shops and API requests. The server may return in the future but for now this app will only display data I have stored over 2 weeks.
**

The API utilized is for the market of a private server for an online game, Ragnarok Online. The goal is to present in-game vending/buying market prices for items, including accumulated historical prices for customizable user accessibility.

Players looking to buy or sell specific items and/or track an item’s value will use the site. There are about 1400+ active players that login to the game’s server each day, plus around 1500 vending shops set-up. There is no auction house and the existing in-game commands for searching the market lack certain functionality and accessibility.

The game server provides an API: https://gitlab.com/originsro/originsro/-/blob/master/doc/api/api_resources.md. It contains data for buying and vending shops that are open in-game (cached every 10 minutes). 

Features:
- Data will be limited to items that are essential to the PvP content meta, meaning specific consumables, cards, gears, and etc items.
- A user can choose which items they want to keep track of. The items will appear on their home page along with the shop and price of the cheapest available stock for it.
- Each item has its own current shops/history page (/tracking/<item_id>) that shows shops currently selling the item, sorted by cheapest price. Below it, the shop details and price of items historically sold in the past 15 days are displayed in order of most recent. The min, max, and average price of the item in the past 15 days are displayed at the top of the page.
- As the API does not provide shop and price history, regular requests are made to store 15 days-worth of data which is then later queried for user features. 
- Data older than 15 days will be deleted as part of the request process.


NOTE: The application can be scaled to include many more if not all items in the game. I narrowed the items down for the project. 

ER Diagram:

![image](https://user-images.githubusercontent.com/68235230/160410726-6363e1d2-635f-4bef-b678-6306ade4ae87.png)

The tables are as follows:

![image](https://user-images.githubusercontent.com/68235230/160411265-84defbd5-716f-47a3-9349-64b96a42a2a1.png)

The many-to-many relationships between User and Item tables and Shops and Item tables are established using the User_Item and Shops_Item tables. 
Note that Shops has two timestamp attributes: timestamp and res_timestamp. res_timestamp is used to distinguish whether a shop has already been added to the database when requesting and filtering data for storage.

Pictures of application:

![image](https://user-images.githubusercontent.com/68235230/189373004-4ac68dce-f5cf-4b1c-aec1-0f6fff623437.png)

![image](https://user-images.githubusercontent.com/68235230/193831909-e91f7c30-92b0-48cd-a1e3-6efcac0bd6bd.png)

![image](https://user-images.githubusercontent.com/68235230/193831838-0d444980-9115-46dc-9d02-f593fd933bd3.png)

![image](https://user-images.githubusercontent.com/68235230/193831512-22ed6a21-f982-4a2a-b13c-c220138df1cd.png)

![image](https://user-images.githubusercontent.com/68235230/193831596-9295c090-a205-42b8-a98c-536590b957cb.png)


Future Changes/Additions:
- Information about armor/weapon refine levels and slotted cards will be implemented. 
- More items will be added according to further research on demand.
- Some additional features include sending the above-mentioned alert through email or Discord, or calculating more item price statistics (standard deviation, etc.) and showing them to the user. The home page could also have statistics on the most popular items. 
- Also, it could be possible to take the minimap for the in-game map a seller is on and set a mark on it using the shop’s x and y coordinates to show where the shop is located.
