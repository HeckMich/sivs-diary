# Intro

 This project is used for the SIVS course at the University of Applied Sciences Burgenland.

Students will attempt to secure a web server and identify security vulnerabilities. 
This application is intentionally insecure and is used as a learning project to help students identify and fix vulnerabilities.

Vulnerabilities included:
XSS, SQLi, missing access control and misconfiguration of the web server.
 

# How to install on Server (AWS Learner Lab)

1. Connect to your server (Ubuntu Instance)
2. Run following commands

```bash
mkdir -p /home/ubuntu/
rm -rf /home/ubuntu/sivs-diary
cd /home/ubuntu/
git clone https://github.com/fhtevssivs/sivs-diary.git
cd sivs-diary/sivs-diary/install/
sudo chmod +x ./install.sh 
sudo ./install.sh
```

# How to run on your local Machine

1. Go to install folder
2. Run `sudo docker compose --env-file ../.env up -d`
3. Setup Python environment and install dependencies from "requirements.txt"
4. Run `python3 create_db.py`

```mermaid
graph LR
    %% Styles definieren
    classDef file fill:#fff,stroke:#333,stroke-width:1px,rx:5,ry:5;
    classDef db fill:#fff,stroke:#333,stroke-width:1px;

    %% --- Backend / Application ---
    subgraph app_folder ["/application"]
        direction TB
        AppPy[app.py]:::file
    end

    %% --- Backend / Source ---
    subgraph src_folder ["/src"]
        direction TB
        
        subgraph api_folder ["/api/"]
            UserMgmt[usermanagement.py]:::file
            DiaryPy[diary.py]:::file
        end
        
        subgraph support_folder ["/support/"]
            DBHandler[db_handler.py]:::file
        end
        
        subgraph pages_py_folder ["/pages/"]
            ViewPy[view.py]:::file
        end
    end

    %% --- Database ---
    Postgres[(PostgresDB)]:::db

    %% --- Frontend ---
    subgraph frontend_folder ["/frontend"]
        direction TB
        
        subgraph pages_html_folder ["/pages/"]
            IndexHtml[index.html]:::file
            CreateAccHtml[create_account.html]:::file
            DiaryHtml[diary.html]:::file
        end
        
        subgraph static_folder ["/static/"]
            MainJs[main.js]:::file
            DiaryJs[diary.js]:::file
            IndexJs[index.js]:::file
            CreateAccJs[create_account.js]:::file
        end
    end

    %% --- Beziehungen / Links ---

    %% Register Links (App -> Modules)
    AppPy -- register --> UserMgmt
    AppPy -- register --> DiaryPy
    AppPy -- register --> ViewPy

    %% Init Links (API -> DB Handler)
    UserMgmt -- init --> DBHandler
    DiaryPy -- init --> DBHandler

    %% Database Link
    DBHandler <-- SQL --> Postgres

    %% View Serving Links
    ViewPy -- serves --> IndexHtml
    ViewPy -- serves --> CreateAccHtml
    ViewPy -- serves --> DiaryHtml

    %% Frontend Assets Links (HTML -> JS)
    %% Index HTML uses
    IndexHtml -- uses --> MainJs
    IndexHtml -- uses --> IndexJs

    %% Create Account HTML uses
    CreateAccHtml -- uses --> MainJs
    CreateAccHtml -- uses --> CreateAccJs

    %% Diary HTML uses
    DiaryHtml -- uses --> MainJs
    DiaryHtml -- uses --> DiaryJs

    %% Link Styles (Optional: Farben anpassen ähnlich dem Bild)
    linkStyle 0,1,2 stroke:#7fcec5,stroke-width:2px;
    linkStyle 3,4 stroke:#f4d03f,stroke-width:2px;
    linkStyle 5 stroke:#5dade2,stroke-width:2px;
    linkStyle 6,7,8 stroke:#a9cce3,stroke-width:2px;
    linkStyle 9,10 stroke:#f1948a,stroke-width:1px;
    linkStyle 11,12 stroke:#d7bde2,stroke-width:1px;
    linkStyle 13,14 stroke:#a9dfbf,stroke-width:1px;
```