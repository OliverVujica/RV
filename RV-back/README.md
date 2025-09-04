# PlantDoctor - Frontend Aplikacija za Prepoznavanje Bolesti Biljaka

Vue.js 3 frontend aplikacija s TailwindCSS stilizacijom koja se povezuje na FastAPI backend za prepoznavanje bolesti biljaka putem AI modela.

## 🚀 Funkcionalnosti

- **Početna stranica** - Objašnjenje aplikacije s mogućnošću anonimnog upload-a
- **Anonimni upload** - Korisnici mogu bez prijave analizirati slike biljaka
- **Autentifikacija** - Registracija i prijava korisnika s JWT tokenima
- **Dashboard** - Upravljanje slikama i pregled povijesti za prijavljene korisnike
- **Responzivan dizajn** - Optimizirano za sve veličine ekrana

## 🛠️ Tehnologije

- **Vue.js 3** s Composition API
- **TailwindCSS** za stilizaciju
- **Vue Router** za routing
- **Pinia** za state management
- **Axios** za API pozive
- **TypeScript** za type safety

## 📦 Instalacija

1. **Klonirajte repozitorij** (ako već nije kloniran)
   ```bash
   git clone [repository-url]
   cd plant-disease-frontend
   ```

2. **Instalirajte dependency-je**
   ```bash
   npm install
   ```

3. **Konfigurirajte environment varijable**
   
   Kreirajte `.env` datoteku u root direktoriju:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Pokrenite development server**
   ```bash
   npm run dev
   ```

5. **Otvorite u browseru**
   
   Aplikacija će biti dostupna na `http://localhost:5173`

## 🏗️ Build za produkciju

```bash
npm run build
```

Generirani fajlovi će se nalaziti u `dist/` direktoriju.

## 📁 Struktura projekta

```
src/
├── components/          # Reusable komponente
│   ├── FileUpload.vue   # Komponenta za upload slika
│   ├── ImageCard.vue    # Prikaz rezultata analize
│   └── Navbar.vue       # Navigacijska traka
├── views/               # Stranice aplikacije
│   ├── Home.vue         # Početna stranica
│   ├── Login.vue        # Stranica za prijavu
│   ├── Register.vue     # Stranica za registraciju
│   └── Dashboard.vue    # Dashboard za korisnike
├── stores/              # Pinia stores
│   └── auth.ts          # Store za autentifikaciju
├── services/            # API servisi
│   └── api.ts           # Axios konfiguracija i API pozivi
├── router/              # Vue Router konfiguracija
│   └── index.ts         # Routing definicije
├── App.vue              # Root komponenta
├── main.ts              # Entry point
└── style.css            # Globalni TailwindCSS stilovi
```

## 🔧 Konfiguracija

### API Endpoint

U `.env` datoteci postavite URL vašeg FastAPI backend servera:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### TailwindCSS

Konfiguracija je u `tailwind.config.js` s custom color paletom:
- Primary boje (zelene tonove)
- Responzivni breakpoint-i
- Custom komponente (`btn-primary`, `btn-secondary`, `input-field`)

## 🔒 Autentifikacija

Aplikacija koristi JWT token autentifikaciju:
- Tokeni se čuvaju u localStorage
- Automatsko uklanjanje pri 401 odgovorima
- Route guards za zaštićene stranice

## 📱 Responzivnost

Aplikacija je optimizirana za:
- **Mobile** (< 768px)
- **Tablet** (768px - 1024px)
- **Desktop** (> 1024px)

## 🎨 UI/UX Komponente

- **FileUpload** - Drag & drop upload s progress indikatorom
- **ImageCard** - Prikaz slika s rezultatima analize
- **Navbar** - Responzivna navigacija s autentifikacijom
- **Grid Layout** - Optimiziran prikaz galerije slika

## 🧪 Development

### Struktura API poziva

Aplikacija očekuje sljedeće API endpoint-e na FastAPI backend-u:

```typescript
POST /auth/login          # Prijava korisnika
POST /auth/register       # Registracija korisnika  
GET  /auth/me             # Dohvaćanje korisničkih podataka
POST /predict/anonymous   # Anonimna analiza slike
POST /predict             # Analiza slike za prijavljene korisnike
GET  /predict/history     # Povijest analiza korisnika
```

### TypeScript tipovi

```typescript
interface User {
  id: string
  email: string
  name: string
}

interface PredictionResult {
  id: string
  image_url: string
  disease: string
  confidence: number
  created_at: string
}
```

## 🤝 Integracija s Backend-om

Aplikacija je dizajnirana za rad s FastAPI backend-om koji treba imati:
- CORS konfiguraciju za frontend origin
- JWT autentifikaciju
- File upload endpoint-e
- MongoDB za čuvanje podataka

Za više informacija o backend konfiguraciji, molimo pogledajte dokumentaciju FastAPI servera.