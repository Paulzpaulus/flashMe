# FlashMe — Projekt-Checkliste

> Tickets aufgebaut auf dem 4-Wochen-Plan des Leads.
> Jedes Ticket baut auf dem vorherigen auf — Reihenfolge einhalten.

---

## WOCHE 1 — Authentication

- [ ] `seed.py` fixen: `User` → `Users` (Import-Bug)
- [ ] `seed.py` erweitern: ersten Admin-User mit `is_admin=True` anlegen
- [ ] Auth-Flow manuell testen: Register → Login → `/me` → Cookie in Browser prüfen
- [ ] Logout-Endpoint implementieren (`POST /logout` → httponly Cookie löschen)
- [ ] Token-Expiry testen: was gibt die API zurück wenn das Cookie abgelaufen ist?
- [ ] Sicherstellen dass alle geschützten Routen ohne Cookie `401` zurückgeben

---

## WOCHE 2 — Schemas & Models vollständig

- [ ] `ai_examples: str | None` Feld zu `Flashcard`-Model hinzufügen
- [ ] `FlashcardCreate` + `FlashcardRead` Schema um `ai_examples` erweitern
- [ ] `SavedDeck` Model erstellen (Tabelle: `user_id`, `deck_id`, composite primary key)
- [ ] `SavedDeck` Schema erstellen (Create + Read)
- [ ] `CardProgress` Model erstellen für SM-2:
  - `user_id` (FK → users)
  - `card_id` (FK → flashcard)
  - `ease_factor` (float, default 2.5)
  - `interval` (int, Tage bis nächstes Review)
  - `repetitions` (int)
  - `next_review` (datetime)
- [ ] DB-Struktur mit Original-Diagram (`docs/preVersion_DB_structure.pdf`) abgleichen
- [ ] Alle Models in `main.py` importieren damit SQLModel die Tabellen anlegt

---

## WOCHE 3 — Endpoints

### Fork / Saved Decks
- [ ] `POST /decks/{id}/save` → öffentliches Deck in eigene Sammlung speichern
- [ ] `GET /decks/saved` → alle gespeicherten Decks des eingeloggten Users
- [ ] `DELETE /decks/{id}/save` → gespeichertes Deck entfernen

### SM-2 Lernmodus
- [ ] `GET /decks/{deck_id}/study` → gibt Karten zurück die heute fällig sind (`next_review <= heute`)
- [ ] `POST /decks/{deck_id}/cards/{card_id}/review` → Bewertung (1–5) entgegennehmen, SM-2-Formel anwenden, `CardProgress` updaten
- [ ] SM-2 Formel implementieren (in `service/` als eigene Funktion, nicht im Router)

### Cleanup & Testing
- [ ] Alle Endpoints in Swagger (`/docs`) vollständig durchklicken
- [ ] Edge Cases prüfen: fremdes privates Deck, nicht existierende IDs, leere Decks lernen

---

## WOCHE 4 — Deployment

- [ ] `.env.example` Datei erstellen (Vorlage ohne echte Werte)
- [ ] `Dockerfile` schreiben
- [ ] Deployment-Plattform wählen (Empfehlung: Railway oder Render — beide haben kostenlosen PostgreSQL-Tier)
- [ ] Produktions-Datenbank einrichten (PostgreSQL hosted)
- [ ] Umgebungsvariablen auf der Plattform setzen
- [ ] Erste erfolgreiche Deployment-Version testen
- [ ] `README.md` mit Deployment-Anleitung aktualisieren

---

## Backlog — Phase 2 (mit Frontend)

- [ ] User Followers / Social Features (`user_followers` Tabelle)
- [ ] Translator-Feature (externe Übersetzungs-API)
- [ ] KI-generierte Beispielsätze für Karten (echter AI-API-Call)
- [ ] Audio- und Datei-Anhänge an Karten
- [ ] Frontend (React / Next.js)
