# Flight Deal Notifier (NYC ➜ Your Destinations)

A Python project that watches flight prices from **NYC** to a list of destinations stored in a **Sheety** spreadsheet.  
It searches the **cheapest flights** over the next ~6 months (direct first, then indirect), and if it finds a deal **below your target price**, it sends a **WhatsApp alert** to your users via **Twilio**.

---

## What It Does
- Pulls destination list + thresholds from a Sheety-powered Google Sheet
- Ensures each destination has an **IATA code** (auto-fills if missing)
- Searches flights within a date window (tomorrow → ~6 months)
- Picks the **cheapest** itinerary (prefers direct; falls back to with stopovers)
- Sends **personalized WhatsApp messages** to your user list when deals are found

---

## Project Structure (Modules)
This project uses several small classes to keep logic clean and testable.

- `data_manager.py` — Read/write to **Sheety**; manages destination rows & user contacts  
- `flight_search.py` — Calls a **flight search API** (e.g., Tequila by Kiwi.com) & refreshes tokens if needed  
- `flight_data.py` — Parses API responses and exposes `find_cheapest_flight()`  
- `notification_manager.py` — Sends **WhatsApp** alerts via **Twilio** (can be extended for email/SMS)  
- `main.py` — Orchestrates the flow (dates, thresholds, notification logic)

---

## Core Flow
1. **Load destinations & users** from Sheety  
2. **(Optional)** Backfill missing IATA codes for each destination city  
3. Compute **date range**: tomorrow → ~6 months out  
4. **Search direct flights** for each destination; pick the **cheapest**  
5. If none found, **search with stopovers**, pick the **cheapest**  
6. If price `< lowestPrice` in your sheet → **send WhatsApp** alert to all users  
7. Log progress & repeat on your own schedule (e.g., cron, GitHub Actions)

---

## WhatsApp Message Example

`Low price alert! Only 275 USD to fly direct from JFK to CDG - Paris,
on 2025-11-03 until 2025-11-12.`

If the best deal includes stops, the message includes:  
`with 1 stop(s) departing on … and returning on …`


