# origins-market-tracker

The API is for the market of a private server for an online game, Ragnarok Online. The goal is to present in-game vending/buying market prices for items, including accumulated historical prices to visualize changes in price. 

Players looking to buy or sell specific items and/or track an item’s value will use the site. There are about 1450 active players that login to the game’s server each day, plus around 1500 vending shops set-up. The existing in-game commands for searching the market lack certain functionality and accessibility so most players would find use for the site.

The game server provides an API: doc/api/api_resources.md · master · OriginsRO / OriginsRO · GitLab. It contains data for buying and vending shops that are open in-game (cached every 10 minutes). 

The database will include user information, static information about items, and historical and current prices along with data on the shops currently selling the item. Customized info like what items are to be tracked will be included as a column under Users.
Market requests are limited to 12 per hour. The plan is to first have static item data stored in the database, then have the dynamic data be requested at intervals of at most 12 times/hour, then finally have users query this stored data. There are tens of thousands of items in the game. The app functionality will be limited to items that are essential to the PvP content meta, meaning specific consumables, cards, gears, and etc items. This list is being compiled and should not be greater than 100 items.
The user’s password and email will need to be secured.
The app will include a user page with information about items they have chosen to track, including previous prices and some statistics to visualize the price fluctuations. Information on where the shops selling each item is located will also be saved to the database and shown to the user.
Some additional features include sending the above-mentioned alert through email or Discord, or calculating more item price statistics (standard deviation, etc.) and showing them to the user. The home page could also have statistics on the most popular items. 
Also, it could be possible to take the minimap for the in-game map a seller is on and set a mark on it using the shop’s x and y coordinates to show where the shop is located.
