# MXBikes Lap Tracker

MXBikes Lap Tracker is een project waarmee je rondetijden van spelers kunt bijhouden en bekijken. Het project bestaat uit drie onderdelen:

1. **Backend**: Django REST API voor het opslaan en ophalen van gebruikers, tracks en rondetijden.
2. **Discord Bot**: Een bot waarmee spelers hun username kunnen instellen en hun rondetijden kunnen toevoegen of bekijken via slash-commands.
3. **Frontend (React)**: Een toekomstige React-app waarmee je per track de rondetijden van alle spelers overzichtelijk kunt bekijken en sorteren.

---

## Features

### Backend

- API voor gebruikers (`User`) en tracks (`Track`)
- Endpoints voor het toevoegen en ophalen van rondetijden (`Lap`)
- Ondersteuning voor ophalen via Discord ID of username
- Validatie van rondetijden in `MM:SS.mmm` formaat
- Makkelijk uitbreidbaar voor extra functionaliteiten

### Discord Bot

- Slash-command `/setusername` om je username in te stellen
- Slash-command `/addlap` om een rondetijd voor een track toe te voegen
- Slash-command `/laps` om alle rondetijden van jezelf of een andere gebruiker op te vragen
- Embed berichten met track, tijd in `MM:SS.mmm` en datum
- Avatar van de gebruiker als thumbnail in de embed

### Frontend (React)

- Toekomstige functionaliteit:
  - Per track overzicht van alle rondetijden
  - Mogelijkheid om te sorteren op tijd
  - Mooie visuele weergave van de data

---
