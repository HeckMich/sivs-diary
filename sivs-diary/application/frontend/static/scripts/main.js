// Funktion zum Senden von JSON-Daten über einen POST-Request
async function postJSON(url, data) {
    console.log(`Zugriff auf URL ${url}`);
    try {
        // Sendet einen POST-Request mit den angegebenen Daten
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Überprüft, ob die Anfrage erfolgreich war
        if (response.ok) {
            // Gibt die JSON-Antwort zurück
            return await response.json();
        } else {
            // Wirft einen Fehler, wenn die Anfrage nicht erfolgreich war
            throw new Error('Anfrage fehlgeschlagen');
        }
    } catch (error) {
        // Behandelt Fehler beim Senden der Anfrage
        console.error("Fehler beim Abrufen der Daten", error);
        throw new Error('Netzwerkantwort war nicht in Ordnung.');
    }
}

// Funktion zum Laden von JSON-Daten über einen GET-Request
async function loadJSON(url) {
    console.log(`Zugriff auf URL ${url}`);
    try {
        // Sendet einen GET-Request
        const response = await fetch(url, {
            method: 'GET'
        });

        // Überprüft, ob die Anfrage erfolgreich war
        if (response.ok) {
            // Gibt die JSON-Antwort zurück
            return await response.json();
        } else {
            // Wirft einen Fehler, wenn die Anfrage nicht erfolgreich war
            throw new Error('Anfrage fehlgeschlagen');
        }
    } catch (error) {
        // Behandelt Fehler beim Laden der Daten
        console.error("Fehler beim Abrufen der Daten", error);
        throw new Error('Netzwerkantwort war nicht in Ordnung.');
    }
}

// Funktion zum Löschen von JSON-Daten über einen DELETE-Request
async function deleteJSON(url, data) {
    console.log(`Zugriff auf URL ${url}`);
    try {
        // Sendet einen DELETE-Request mit den angegebenen Daten
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Überprüft, ob die Anfrage erfolgreich war
        if (response.ok) {
            // Gibt die JSON-Antwort zurück
            return await response.json();
        } else {
            // Wirft einen Fehler, wenn die Anfrage nicht erfolgreich war
            throw new Error('Anfrage fehlgeschlagen');
        }
    } catch (error) {
        // Behandelt Fehler beim Löschen der Daten
        console.error("Fehler beim Löschen der Daten", error);
        throw new Error('Netzwerkantwort war nicht in Ordnung.');
    }
}
