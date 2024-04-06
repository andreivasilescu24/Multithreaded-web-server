Nume: Vasilescu Andrei

Grupă: 334 CD

# Tema 1 - Le Stats Sportif

## 1. Solutie

Solutia implementata va crea serverul Flask, impreuna cu un DataIngestor si un ThreadPool. Pe masura ce se primesc request-uri pe endpoint-urile din enunt, functiile de
handle pentru aceste rute vor trimite catre ThreadPool noul task primit, in cazul in care sunt request-uri POST. In cazul in care sunt request-uri GET nu se va face un
nou job ID si nici nu se va pune in coada un job deoarece fie este nevoie de un rezultat din momentul respectiv cum ar fi statusul job-urilor din ThreadPool, numarul
de joburi in "running" sau rezultatul unui job este nevoie de inchiderea server-ului si implicit a ThreadPool-ului care nu va mai accepta niciun fel de task. Astfel, 
doar request-urile unde se doreste calcularea unei statistici vor primi un job ID si vor adauga un task in coada deoarece se doreste sa avem functionalitatea de a afla 
status-urile job-urilor sau numarul de joburi in running si dupa ce s-a dat shutdown la server fiindca ThreadPool-ul va continua sa ruleze toate task-urile care au ramas 
in coada si dupa shutdown. 

In urma primirii unui nou job, se va intoarce un JSON cu job ID-ul noului task si se va incrementa job ID-ul pentru un urmator task. ThreadPool-ul il va adauga in coada sa 
de unde un thread il va putea accesa si executa scriind rezultatul in fisierul JSON cu numele corespunzator job-ului rulat. Am utilizat aceasta solutie de scriere in 
fisiere a rezultatelor pentru a nu stoca cantitati mari de date in structuri de date precum dictionare/liste si pentru a fi usor de accesat (prin citirea continutului fisierului) 
in momentul in care se primeste un request ce doreste sa primeasca rezultatul unui anume job.

Consider ca tema este una utila deoarece prin ea am consolidat mai bine conceptele din spatele unui server multithreaded, dar si mecanismele de sincronizare si importanta acestora 
intr-o aplicatie de acest gen. De asemenea, aceasta aplicatie este una utila deoarece ofera intr-un timp rezonabil statistici pentru un set de date de dimensiuni foarte mari. In opinia 
mea, am folosit o implementare eficienta, deoarece thread-urile executa in paralel task-urile din coada ceea ce optimizeaza server-ul, dar si pentru ca rezultatele finale sunt stocate
in fisere, nu in interiorul unor structuri de date din ThreadPool, deoarece acestea pot ajunge la dimensiuni mult prea mari ceea ce ar afecta eficienta in ceea ce priveste memoria.

## 2. Implementare

Am implementat in intregime enuntul temei.

In ThreadPool voi retine informatii despre fiecare job care intra in coada de executie, avand trei dictionare in care fiecare job ID (cheia) are asociat ca valoare statusul, JSON-ul 
cu care a venit request-ul pentru a il putea da mai departe catre functiile de statistica, dar si tipul de job ("states_mean", "global_mean", etc.) pentru ca fiecare thread sa stie ce
functie sa apeleze pentru a obtine rezultatul. De asemenea, pe langa coada de job-uri si dictionarele acestea, ThreadPool-ul mai are o lista cu thread-urile create, un event pentru
momentul cand se da shutdown si un lock pentru a evita accesul concurent la dictionare pe un job anume (spre exemplu se primeste un request de GET pentru a afla statusul job-urilor asa
ca voi folosi lock-ul pe dicitionar, pentru a obtine status-ul din momentul respectiv, deoarece exista posibilitatea ca intre timp un thread sa termine executia unui job si sa updateze
statusul la "done" ceea ce va afecta rezultatul request-ului, asa ca thread-ul va astepta pana va putea lua Lock-ul ca sa schimbe statusul). Toate aceste structuri de date, dar si
mecanisme de sincronizare sunt date ca parametru fiecarui thread pentru ca acestea sa se poata folosi de ele.

In momentul in care se va cere shutdown-ul se va seta Eventul si astfel toate thread-urile vor putea fi "notificate" ca urmeaza inchiderea si ca ar trebui sa isi termine rularea cat
mai repede, dupa ce nu mai exista job-uri de executat in coada. De asemenea, functia de shutdown din ThreadPool va astepta terminarea tuturor thread-urilor inainte de inchidere.

Fiecare thread din ThreadPool va rula pana cand se va cere shutdown-ul server-ului si coada de job-uri va fi goala, astfel fiecare thread incearca sa preia din coada un job
pentru a il rula, insa nu se blocheaza mai mult de 2 secunde, iar daca coada e goala va verifica daca s-a cerut shutdown-ul, in caz afirmativ inchizandu-se. Am creat acest
mecanism deoarece exista si cazul in care server-ul se porneste si se cere un shutdown imediat, astfel daca toate thread-urile erau blocate in incercarea de a prelua un task,
acestea rulau la infinit, chiar daca server-ul s-a inchis si nu vor mai intra alte task-uri. Cand un thread reuseste sa preia un task acesta va apela functia de calculare de
statistici corespunzatoare job-ului si va scrie rezultatul in fisierul JSON. Am folosit "eval" pentru a apela functiile corespunzatoare tipului de cerere al fiecarui job ID
ce este retinut in dictionarul creat in ThreadPool si care este updatat de fiecare data cand se introduce un nou task. Dupa ce va fi scris rezultatul statisticii in fisier,
thread-ul va updata statusul pentru job ID-ul rulat la "done" cu ajutorul unui Lock pe dictionarul cu statusuri ce este partajat de toate thread-urile.

In ceea ce priveste functiile care calculeaza rezultatele si opereaza pe CSV-ul primit ("states_mean", "mean_by_category", etc.) acestea se afla in DataIngestor pentru a
putea accesa cu usurinta tabelul CSV citit. Rezultatele operatiilor pe CSV sunt obtinute cu ajutorul operatiilor puse la dispoztie de "pandas" deoarece sunt usor de folosit,
iar pentru cantitati mari de date cum sunt in CSV-ul utilizat in tema, consider ca este mai eficient sa folosim o biblioteca dedicata acestor tipuri de operatii. De asemenea,
functiile de calcul a statisticilor din acest fisier au acelasi nume cu tipul de request pe care il satisfac pentru a putea fi apelate cu "eval" din thread-uri.

De asemenea, am creat si functia de logging pentru a monitoriza activitatea de pe server, astfel in fisierul "webserver.log" se vor gasi toate request-urile de la rularea
server-ului, impreuna cu un timestamp, cu endpoint-ul catre care s-a executat request-ul dar si un mesaj sugestiv pentru actiunea facuta. Se vor loga si startul si inchiderea
serverului, precum si erorile precum adaugarea unui task dupa shutdown.

Am creat unitteste pentru rezultatele returnate de functiile de statistica din DataIngestor pentru a valida corectitudinea acestora. Acestea insa vor rula pe un CSV de
dimensiuni mult mai reduse decat cel pe care opereaza server-ul.

#### Dificultăți întâmpinate

- Erori de circular import intre fisiere
- Asteptarea la infinit a unor thread-uri pentru un job chiar si dupa shutdown

#### Lucruri interesante descoperite pe parcurs

- Functia de "eval" ce poate apela o functie cu numele retinut intr-un string


### Resurse utilizate

- https://ocw.cs.pub.ro/courses/asc/laboratoare/02
- https://ocw.cs.pub.ro/courses/asc/laboratoare/03
- https://docs.python.org/3/library/unittest.html#organizing-test-code
- https://docs.python.org/3/library/logging.html
- https://stackoverflow.com/questions/24722212/python-cant-find-module-in-the-same-folder
- https://www.toppr.com/guides/python-guide/references/methods-and-functions/methods/built-in/eval/python-eval/
- https://docs.python.org/3/library/queue.html

### Git

https://github.com/andreivasilescu24/Tema1-ASC