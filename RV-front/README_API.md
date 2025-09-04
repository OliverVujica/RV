# API Dokumentacija

### 1. Registracija Korisnika (POST `/register`)

**Zahtjev:**
```json
{
    "username": "korisnicko_ime",
    "email": "email@primer.com", 
    "password": "JakaLozinka123",
    "password_confirmation": "JakaLozinka123"
}
```

**Validacija:**
- **username**: 3-50 karaktera, samo slova, brojevi, tačke, crtica i donja crtica
- **email**: Valjan email format
- **password**: Minimum 8 karaktera, mora sadržavati:
  - Najmanje jedno veliko slovo
  - Najmanje jedno malo slovo  
  - Najmanje jedan broj
- **password_confirmation**: Mora se poklapati sa password poljem

**Odgovor (uspjeh):**
```json
{
    "message": "User created successfully"
}
```

**Moguće greške:**
- `400`: "Username already exists"
- `400`: "Email already exists"
- `422`: Validation errors (passwords don't match, weak password, invalid email, etc.)

### 2. Prijava (POST `/token`)

Korisnik se može prijaviti pomoću **username-a** ili **email-a**:

**Zahtjev (form data):**
```
username: korisnicko_ime ili email@primer.com
password: JakaLozinka123
```

**Odgovor:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 3. Profil Korisnika (GET `/profile`)

**Zahtjev:**
- Potreban `Authorization: Bearer <token>` header

**Odgovor:**
```json
{
    "username": "korisnicko_ime",
    "email": "email@primer.com",
    "user_id": "60f7b3b3b3b3b3b3b3b3b3b3"
}
```

## Pokretanje Servera

```bash
uvicorn main:app --reload
```

Server će biti dostupan na: http://localhost:8000

## Testiranje

**Registracija:**
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com", 
       "password": "TestPass123",
       "password_confirmation": "TestPass123"
     }'
```

**Prijava:**
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=TestPass123"
```

**Profil:**
```bash
curl -X GET "http://localhost:8000/profile" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Baza Podataka

Korisnici se čuvaju u MongoDB kolekciji `users` sa sljedećom strukturom:

```json
{
    "_id": ObjectId("..."),
    "username": "korisnicko_ime",
    "email": "email@primer.com",
    "password": "$2b$12$hashed_password..."
}
```

## Sigurnosne Mjere

1. **Password hashing**: Koristi se bcrypt
2. **JWT tokeni**: Sa expiracijom od 30 minuta
3. **Email validacija**: Provjerava format email adrese
4. **Password strength**: Zahtjeva jake lozinke
5. **Unique constraints**: Username i email moraju biti jedinstveni
