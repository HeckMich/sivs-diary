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
    %% --- STYLING DEFINITONEN ---
    classDef file fill:#ffffff,stroke:#4a69bd,stroke-width:2px,rx:10,ry:10,color:#2c3e50,font-family:sans-serif;
    classDef db fill:#fff3e0,stroke:#e67e22,stroke-width:3px,rx:5,ry:5,color:#d35400,font-family:sans-serif;
    style app_folder fill:#f4f7f6,stroke:#bdc3c7,stroke-width:1px,color:#7f8c8d
    style src_folder fill:#f4f7f6,stroke:#bdc3c7,stroke-width:1px,color:#7f8c8d
    style frontend_folder fill:#f4f7f6,stroke:#bdc3c7,stroke-width:1px,color:#7f8c8d
    style api_folder fill:#ffffff,stroke:#ecf0f1,color:#95a5a6
    style support_folder fill:#ffffff,stroke:#ecf0f1,color:#95a5a6
    style pages_py_folder fill:#ffffff,stroke:#ecf0f1,color:#95a5a6
    style pages_html_folder fill:#ffffff,stroke:#ecf0f1,color:#95a5a6
    style static_folder fill:#ffffff,stroke:#ecf0f1,color:#95a5a6


    %% --- STRUKTUR ---

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

    %% --- BEZIEHUNGEN / LINKS ---

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
    IndexHtml -- uses --> MainJs
    IndexHtml -- uses --> IndexJs
    CreateAccHtml -- uses --> MainJs
    CreateAccHtml -- uses --> CreateAccJs
    DiaryHtml -- uses --> MainJs
    DiaryHtml -- uses --> DiaryJs

    %% --- LINK STYLING ---
    linkStyle 0,1,2,3,4 stroke:#6c5ce7,stroke-width:2px,fill:none;
    linkStyle 5 stroke:#e67e22,stroke-width:3px,fill:none;
    linkStyle 6,7,8 stroke:#00cec9,stroke-width:2px,fill:none;
    linkStyle 9,10,11,12,13,14 stroke:#e84393,stroke-width:2px,fill:none;
```