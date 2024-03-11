Töö ülesandepüstitus: https://docs.google.com/document/d/1TGXq2MJIGIlj1cWIJ8RT5CsCHbxPEKXoB6gS2QEl6eg/edit?usp=sharing

# Build
```cd loputoo-2024```

```docker build -t msi-adrift .```

# Run
```docker run --rm -p 5000:5000 msi-adrift```

or

```docker-compose up --build -d```

In browser go to `https://localhost:5000`