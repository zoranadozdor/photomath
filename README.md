# photomath

Projekt sam radila u PyCharmu. 
Program se može pokreniti s main.py (za učitati sliku) ili s app.py (za korištenje kamere). 
Za pokretanje s Dockerom treba izvršiti naredbu docker-compose up ( doduše imala sam problema s otvaranjem kamere kad pokrećem s Dockerom.. )
Trenirala sam jednostavan model na bazi podataka skinutoj s interneta (slike za treniranje nisam priložila zbog memorije :)).
Priložila sam i dva jednostavna primjera za koje model točno računa izraz. 

Moguća poboljšanja: 
    - istrenirati bolji model, na više slika za učenje
    - napraviti robusniju detekciju kontura brojeva
    - popraviti Docker
