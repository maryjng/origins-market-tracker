# origins-market-tracker

Tools used:  Python/Flask, PostgreSQL, SQLAlchemy, Jinja, RESTful API, HTML, CSS

The API is for the market of a private server for an online game, Ragnarok Online. The goal is to present in-game vending/buying market prices for items, including accumulated historical prices to document changes in price. 

Players looking to buy or sell specific items and/or track an item’s value will use the site. There are about 1400+ active players that login to the game’s server each day, plus around 1500 vending shops set-up. There is no auction house and the existing in-game commands for searching the market lack certain functionality and accessibility.

The game server provides an API: doc/api/api_resources.md · master · OriginsRO / OriginsRO · GitLab. It contains data for buying and vending shops that are open in-game (cached every 10 minutes). 


Features:
- Data will be limited to items that are essential to the PvP content meta, meaning specific consumables, cards, gears, and etc items.
- Data older than 15 days will be deleted.
- A user can choose which items they want to keep track of. The items will appear on their home page along with the shop and price of the cheapest available stock for it.
- Each item has its own current shops/history page (/tracking/<item_id>) that shows shops currently selling the item, sorted by cheapest price. Below it, the shop details and price of items historically sold in the past 15 days are displayed in order of most recent. The min, max, and average price of the item in the past 15 days are displayed at the top of the page.


Future Changes/Additions:
- Information about armor/weapon refine levels and slotted cards will be implemented. 
- More items will be added according to further research on demand.

- Some additional features include sending the above-mentioned alert through email or Discord, or calculating more item price statistics (standard deviation, etc.) and showing them to the user. The home page could also have statistics on the most popular items. 
- Also, it could be possible to take the minimap for the in-game map a seller is on and set a mark on it using the shop’s x and y coordinates to show where the shop is located.
