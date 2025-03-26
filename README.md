# origins-market-tracker

## Tools used:  Python/Flask, PostgreSQL, SQLAlchemy, Jinja, API, HTML, CSS

** NOTE **
08/22/2024
The server is back! Still waiting on the API to return as well. Looking back at this code, there is a lot of refactoring and improving to do. I may transform this project to integrate with other tools like Discord.. at least for personal use. 
I am aiming to include all items in this application this time.
**

## Summary

The API utilized is for the market of a private server for an online game, Ragnarok Online. The goal is to present in-game vending/buying market prices for items, including accumulated historical prices for customizable user accessibility.

Players looking to buy or sell specific items and/or track an item’s value will use the site. There are about 1400+ active players that login to the game’s server each day, plus around 1500 vending shops set-up. There is no auction house and the existing in-game commands for searching the market lack certain functionality and accessibility.

The game server provides an API: https://gitlab.com/originsro/originsro/-/blob/master/doc/api/api_resources.md. It contains data for buying and vending shops that are open in-game (cached every 10 minutes). 

## Features
- Data will be limited to items that are essential to the PvP content meta, meaning specific consumables, cards, gears, and etc items.
- A user can choose which items they want to keep track of. The items will appear on their home page along with the shop and price of the cheapest available stock for it.
- Each item has its own current shops/history page (/tracking/<item_id>) that shows shops currently selling the item, sorted by cheapest price. Below it, the shop details and price of items historically sold in the past 15 days are displayed in order of most recent. The min, max, and average price of the item in the past 15 days are displayed at the top of the page.
- As the API does not provide shop and price history, regular requests are made to store 15 days-worth of data which is then later queried for user features. 
- Data older than 15 days will be deleted as part of the request process.


NOTE: The application can be scaled to include many more if not all items in the game. I narrowed the items down for the project. 

Planned table changes:
![image](https://github.com/user-attachments/assets/2e9af571-7e56-40ec-bc89-da83ba749f68)

---

# API Documentation: Tracking App

This API provides endpoints for user authentication, session management, and item tracking.

## Authentication & User Management

### Login
**Endpoint:** `POST /login`  
**Description:** Authenticates a user and starts a session.  
**Request Body:**  
```json
{
  "username": "example_user",
  "password": "securepassword"
}
```
**Response:**  
- `302 Found` → Redirects to `/` on success.  
- `200 OK` → Renders login form on failure.  

---

### Register
**Endpoint:** `POST /register`  
**Description:** Registers a new user.  
**Request Body:**  
```json
{
  "username": "new_user",
  "email": "user@example.com",
  "password": "securepassword"
}
```
**Response:**  
- `302 Found` → Redirects to `/tracking` on success.  
- `200 OK` → Renders registration form with error message if username exists.  

---

### Logout
**Endpoint:** `GET /logout`  
**Description:** Logs the user out and clears session data.  
**Response:**  
- `302 Found` → Redirects to `/`.  

---

## Item Tracking

### Get Tracked Items
**Endpoint:** `GET /tracking`  
**Description:** Fetches all tracked items for the logged-in user.  
**Response:**  
- `200 OK` → Renders a list of tracked items.  
- `302 Found` → Redirects to `/login` if unauthorized.  

---

### Add Item to Tracking
**Endpoint:** `POST /tracking/add`  
**Description:** Adds an item to the user’s tracking list.  
**Request Body:**  
```json
{
  "item_id": 123
}
```
**Response:**  
- `200 OK` → Displays confirmation message.  
- `302 Found` → Redirects to `/` if unauthorized.  

---

### Get Item Tracking Details
**Endpoint:** `GET /tracking/{id}`  
**Description:** Retrieves historical and current prices for a tracked item.  
**Path Parameter:**  
- `id` (integer) → The ID of the item.  
**Response:**  
- `200 OK` → Renders item details and price statistics.  
- `302 Found` → Redirects to `/login` if unauthorized.  

---

### Remove Item from Tracking
**Endpoint:** `POST /tracking/{id}/remove`  
**Description:** Removes an item from the user’s tracking list.  
**Path Parameter:**  
- `id` (integer) → The ID of the item to remove.  
**Response:**  
- `302 Found` → Redirects to `/tracking` after removal.  
- `302 Found` → Redirects to `/login` if unauthorized.  

---

# Relational Database and ER Diagram

ER Diagram:

![image](https://user-images.githubusercontent.com/68235230/160410726-6363e1d2-635f-4bef-b678-6306ade4ae87.png)

The tables are as follows:

![image](https://user-images.githubusercontent.com/68235230/160411265-84defbd5-716f-47a3-9349-64b96a42a2a1.png)

The many-to-many relationships between User and Item tables and Shops and Item tables are established using the User_Item and Shops_Item tables. 
Note that Shops has two timestamp attributes: timestamp and res_timestamp. res_timestamp is used to distinguish whether a shop has already been added to the database when requesting and filtering data for storage.

---

# Pictures of Application and Future Changes

![image](https://user-images.githubusercontent.com/68235230/210119273-8a596b05-8b9e-4c22-b098-8e1bf9c994e9.png)

![image](https://user-images.githubusercontent.com/68235230/210118218-414714af-34c3-49c8-a24c-11813c91ff6d.png)

![image](https://user-images.githubusercontent.com/68235230/210119289-5be94f68-42c2-4e63-92ff-0542b3a6c94c.png)

![image](https://user-images.githubusercontent.com/68235230/210119237-ee6a80b0-7759-4f0c-a3da-e18f1f3d0fad.png)

![image](https://user-images.githubusercontent.com/68235230/210119251-10ab89cb-ea26-4dfb-ad41-437fbe81c6a5.png)

Future Changes/Additions (If the server comes back up):
- Information about armor/weapon refine levels and slotted cards will be implemented. 
- More items will be added according to further research on demand.
- Some additional features include sending the above-mentioned alert through email or Discord, or calculating more item price statistics (standard deviation, etc.) and showing them to the user. The home page could also have statistics on the most popular items. 
- Also, it could be possible to take the minimap for the in-game map a seller is on and set a mark on it using the shop’s x and y coordinates to show where the shop is located.
