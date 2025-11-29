const form = document.getElementById("createAccountForm");

// Hilfsfunktion: Zeigt eine Fehlermeldung im Formular an
const zeigeFehler = (nachricht) => {
    const alertId = 'alert';
    const formContainer = document.getElementById('createAccountForm');

    // Entfernt existierende Warnungen, um Duplikate zu vermeiden
    const vorhandeneWarnung = document.getElementById(alertId);
    if (vorhandeneWarnung) {
        vorhandeneWarnung.remove();
    }

    // Erstellt das neue Warnungselement
    const warnungsfeld = document.createElement('div');
    warnungsfeld.innerHTML = nachricht;
    warnungsfeld.id = alertId;
    warnungsfeld.classList.add("alert", "alert-danger", "border-danger");
    
    // Fügt die Warnung dem Container hinzu
    formContainer.appendChild(warnungsfeld);
};

form.addEventListener("submit", async function (event) {
    // Verhindert das Standardverhalten (Seite neu laden)
    event.preventDefault();

    // Werte aus den Feldern holen
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const secretQuestion = document.getElementById("secret_question").value;
    const secretAnswer = document.getElementById("secret_answer").value;

    // Überprüfung: Sind alle Felder ausgefüllt?
    if (!username || !password || !secretQuestion || !secretAnswer) {
        zeigeFehler("Bitte füllen Sie alle Felder aus.");
        return; // Bricht die Funktion hier ab
    }

    // Daten für die API vorbereiten (Kurzschreibweise)
    const registerData = { username, password, secretQuestion, secretAnswer };
    const loginData = { username, password };

    try {
        // 1. Benutzer erstellen
        await postJSON('/api/createuser', registerData);

        // 2. Automatisch einloggen (Authorize)
        const response = await postJSON('/api/authorize', loginData);

        // 3. Weiterleitung bei Erfolg
        window.location.href = response.homelink;

    } catch (error) {
        console.error("Registrierungsfehler:", error);
        // Optional: Zeige die genaue Fehlermeldung vom Server, falls vorhanden, sonst Standardtext
        const fehlermeldung = "Fehler beim Erstellen des Benutzerkontos.";
        zeigeFehler(fehlermeldung);
    }
});